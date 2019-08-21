from trezor import loop, utils, wire
from trezor.crypto.hashlib import sha256
from trezor.errors import IdentifierMismatchError, MnemonicError, ShareAlreadyAddedError
from trezor.messages.Success import Success

from . import recover

from apps.common import mnemonic, storage
from apps.common.layout import show_success
from apps.management.recovery_device import layout

if False:
    from typing import List


async def recovery_homescreen() -> None:
    # recovery process does not communicate on the wire
    ctx = wire.DummyContext()
    try:
        await recovery_process(ctx)
    finally:
        # clear the loop state, so loop.run will exit
        loop.clear()
        # clear the registered wire handlers to avoid conflicts
        wire.clear()


async def recovery_process(ctx: wire.Context) -> Success:
    try:
        result = await _continue_recovery_process(ctx)
    except recover.RecoveryAborted:
        dry_run = storage.recovery.is_dry_run()
        if dry_run:
            storage.recovery.end_progress()
        else:
            storage.wipe()
        raise wire.ActionCancelled("Cancelled")
    return result


async def _continue_recovery_process(ctx: wire.Context) -> Success:
    # gather the current recovery state from storage
    in_progress = storage.recovery.is_in_progress()
    word_count = storage.recovery.get_word_count()
    dry_run = storage.recovery.is_dry_run()

    if not in_progress:  # invalid and inconsistent state
        raise RuntimeError
    if not word_count:  # the first run, prompt word count from the user
        word_count = await _request_and_store_word_count(ctx, dry_run)

    mnemonic_type = mnemonic.type_from_word_count(word_count)

    secret = await _request_secret(ctx, word_count, mnemonic_type)

    if dry_run:
        result = await _finish_recovery_dry_run(ctx, secret, mnemonic_type)
    else:
        result = await _finish_recovery(ctx, secret, mnemonic_type)
    return result


async def _finish_recovery_dry_run(
    ctx: wire.Context, secret: bytes, mnemonic_type: int
) -> Success:
    digest_input = sha256(secret).digest()
    stored = mnemonic.get_secret()
    digest_stored = sha256(stored).digest()
    result = utils.consteq(digest_stored, digest_input)

    # Check that the identifier and iteration exponent match as well
    if mnemonic_type == mnemonic.TYPE_SLIP39:
        result &= (
            storage.device.get_slip39_identifier()
            == storage.recovery.get_slip39_identifier()
        )
        result &= (
            storage.device.get_slip39_iteration_exponent()
            == storage.recovery.get_slip39_iteration_exponent()
        )

    await layout.show_dry_run_result(ctx, result, mnemonic_type)

    storage.recovery.end_progress()

    if result:
        return Success("The seed is valid and matches the one in the device")
    else:
        raise wire.ProcessError("The seed does not match the one in the device")


async def _finish_recovery(
    ctx: wire.Context, secret: bytes, mnemonic_type: int
) -> Success:
    storage.device.store_mnemonic_secret(
        secret, mnemonic_type, needs_backup=False, no_backup=False
    )
    if mnemonic_type == mnemonic.TYPE_SLIP39:
        identifier = storage.recovery.get_slip39_identifier()
        exponent = storage.recovery.get_slip39_iteration_exponent()
        if identifier is None or exponent is None:
            # Identifier and exponent need to be stored in storage at this point
            raise RuntimeError
        storage.device.set_slip39_identifier(identifier)
        storage.device.set_slip39_iteration_exponent(exponent)

    await show_success(ctx, ("You have successfully", "recovered your wallet."))

    storage.recovery.end_progress()
    return Success(message="Device recovered")


async def _request_and_store_word_count(ctx: wire.Context, dry_run: bool) -> int:
    homepage = layout.RecoveryHomescreen("Select number of words")
    await layout.homescreen_dialog(ctx, homepage, "Select")

    # ask for the number of words
    word_count = await layout.request_word_count(ctx, dry_run)

    # save them into storage
    storage.recovery.set_word_count(word_count)

    return word_count


async def _request_secret(
    ctx: wire.Context, word_count: int, mnemonic_type: int
) -> bytes:
    await _request_share_first_screen(ctx, word_count, mnemonic_type)

    secret = None
    while secret is None:
        # ask for mnemonic words one by one
        group_count = storage.recovery.get_slip39_group_count()
        if group_count:
            group_threshold = storage.recovery.get_slip39_group_threshold()
            shares_remaining = storage.recovery.get_slip39_shares_remaining()
            advanced_shamir = group_count > 1
            mnemonics = storage.recovery_shares.fetch(group_count)
        else:
            mnemonics = storage.recovery_shares.fetch()
            advanced_shamir = False

        if advanced_shamir:
            await _show_remaining_groups_and_shares(
                ctx, group_threshold, mnemonics, shares_remaining
            )

        try:
            words = await layout.request_mnemonic(
                ctx, word_count, mnemonic_type, mnemonics, advanced_shamir
            )
        except IdentifierMismatchError:
            await layout.show_identifier_mismatch(ctx)
            continue
        except ShareAlreadyAddedError:
            await layout.show_share_already_added(ctx)
            continue
        # process this seed share
        try:
            secret = recover.process_share(words, mnemonic_type)
        except MnemonicError:
            await layout.show_invalid_mnemonic(ctx, mnemonic_type)
            continue
        if secret is None:
            await _request_share_next_screen(ctx, mnemonic_type)

    return secret


async def _request_share_first_screen(
    ctx: wire.Context, word_count: int, mnemonic_type: int
) -> None:
    if mnemonic_type == mnemonic.TYPE_BIP39:
        content = layout.RecoveryHomescreen(
            "Enter recovery seed", "(%d words)" % word_count
        )
        await layout.homescreen_dialog(ctx, content, "Enter seed")
    elif mnemonic_type == mnemonic.TYPE_SLIP39:
        remaining = storage.recovery.get_remaining()
        if remaining:
            await _request_share_next_screen(ctx, mnemonic_type)
        else:
            content = layout.RecoveryHomescreen(
                "Enter any share", "(%d words)" % word_count
            )
            await layout.homescreen_dialog(ctx, content, "Enter share")
    else:
        raise RuntimeError


async def _request_share_next_screen(ctx: wire.Context, mnemonic_type: int) -> None:
    if mnemonic_type == mnemonic.TYPE_SLIP39:
        remaining = storage.recovery.get_remaining()
        shares_remaining = storage.recovery.get_slip39_shares_remaining()
        if not remaining:
            # 'remaining' should be stored at this point
            raise RuntimeError
        if shares_remaining and len(shares_remaining.strip(b"\x00")) > 0:
            content = layout.RecoveryHomescreen(
                "More shares needed", "for this recovery"
            )
            await layout.homescreen_dialog(ctx, content, "Enter share")
        else:
            if remaining == 1:
                text = "1 more share"
            else:
                text = "%d more shares" % remaining
            content = layout.RecoveryHomescreen(text, "needed to enter")
            await layout.homescreen_dialog(ctx, content, "Enter share")
    else:
        raise RuntimeError


async def _show_remaining_groups_and_shares(
    ctx: wire.Context,
    group_threshold: int,
    mnemonics: List[str],
    shares_remaining: bytearray,
) -> None:
    identifiers = []
    for m in mnemonics:
        identifier = " ".join(
            m.split(" ")[0:3]
        )  # TODO: is there a betterway to do this?
        identifiers.append(identifier)
        # list only unique identifiers
        identifiers = list(set(identifiers))
        # remove default remainig values from bytearray
        # the remaining values correspond to remaining shares in identifiers in order
        shares_remaining = shares_remaining.strip(b"\x10")
    return await layout.show_remaining_shares(
        ctx, identifiers, group_threshold, shares_remaining
    )
