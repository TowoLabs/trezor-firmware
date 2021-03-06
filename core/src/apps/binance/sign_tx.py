from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.messages import MessageType
from trezor.messages.BinanceCancelMsg import BinanceCancelMsg
from trezor.messages.BinanceOrderMsg import BinanceOrderMsg
from trezor.messages.BinanceSignedTx import BinanceSignedTx
from trezor.messages.BinanceTransferMsg import BinanceTransferMsg
from trezor.messages.BinanceTxRequest import BinanceTxRequest

from apps.binance import CURVE, helpers, layout
from apps.common import paths


async def sign_tx(ctx, envelope, keychain):
    # create transaction message -> sign it -> create signature/pubkey message -> serialize all
    if envelope.msg_count > 1:
        raise ValueError("Multiple messages not supported")
    await paths.validate_path(
        ctx, helpers.validate_full_path, keychain, envelope.address_n, CURVE
    )

    node = keychain.derive(envelope.address_n)

    tx_req = BinanceTxRequest()

    msg = await ctx.call_any(
        tx_req,
        MessageType.BinanceCancelMsg,
        MessageType.BinanceOrderMsg,
        MessageType.BinanceTransferMsg,
    )

    msg_json = helpers.produce_json_for_signing(envelope, msg)

    if isinstance(msg, BinanceTransferMsg):
        await layout.require_confirm_transfer(ctx, msg)
    elif isinstance(msg, BinanceOrderMsg):
        await layout.require_confirm_order(ctx, msg)
    elif isinstance(msg, BinanceCancelMsg):
        await layout.require_confirm_cancel(ctx, msg)
    else:
        raise ValueError("input message unrecognized, is of type " + type(msg).__name__)

    signature_bytes = generate_content_signature(msg_json.encode(), node.private_key())

    return BinanceSignedTx(signature=signature_bytes, public_key=node.public_key())


def generate_content_signature(json: bytes, private_key: bytes) -> bytes:
    msghash = sha256(json).digest()
    return secp256k1.sign(private_key, msghash)[1:65]
