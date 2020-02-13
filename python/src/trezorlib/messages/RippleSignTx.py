# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .RippleAccountDelete import RippleAccountDelete
from .RippleAccountSet import RippleAccountSet
from .RippleCheckCancel import RippleCheckCancel
from .RippleCheckCash import RippleCheckCash
from .RippleCheckCreate import RippleCheckCreate
from .RippleDepositPreauth import RippleDepositPreauth
from .RippleEscrowCancel import RippleEscrowCancel
from .RippleEscrowCreate import RippleEscrowCreate
from .RippleEscrowFinish import RippleEscrowFinish
from .RippleMemo import RippleMemo
from .RippleOfferCancel import RippleOfferCancel
from .RippleOfferCreate import RippleOfferCreate
from .RipplePayment import RipplePayment
from .RipplePaymentChannelClaim import RipplePaymentChannelClaim
from .RipplePaymentChannelCreate import RipplePaymentChannelCreate
from .RipplePaymentChannelFund import RipplePaymentChannelFund
from .RippleSetRegularKey import RippleSetRegularKey
from .RippleSigner import RippleSigner
from .RippleSignerListSet import RippleSignerListSet
from .RippleTrustSet import RippleTrustSet

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleSignTx(p.MessageType):
    MESSAGE_WIRE_TYPE = 402

    def __init__(
        self,
        address_n: List[int] = None,
        fee: int = None,
        flags: int = None,
        sequence: int = None,
        last_ledger_sequence: int = None,
        account_txn_id: str = None,
        memos: List[RippleMemo] = None,
        signers: List[RippleSigner] = None,
        source_tag: int = None,
        account: str = None,
        signing_pub_key: str = None,
        account_set: RippleAccountSet = None,
        check_cancel: RippleCheckCancel = None,
        check_cash: RippleCheckCash = None,
        check_create: RippleCheckCreate = None,
        deposit_preauth: RippleDepositPreauth = None,
        escrow_cancel: RippleEscrowCancel = None,
        escrow_create: RippleEscrowCreate = None,
        escrow_finish: RippleEscrowFinish = None,
        offer_cancel: RippleOfferCancel = None,
        offer_create: RippleOfferCreate = None,
        payment: RipplePayment = None,
        payment_channel_claim: RipplePaymentChannelClaim = None,
        payment_channel_create: RipplePaymentChannelCreate = None,
        payment_channel_fund: RipplePaymentChannelFund = None,
        set_regular_key: RippleSetRegularKey = None,
        signer_list_set: RippleSignerListSet = None,
        trust_set: RippleTrustSet = None,
        account_delete: RippleAccountDelete = None,
    ) -> None:
        self.address_n = address_n if address_n is not None else []
        self.fee = fee
        self.flags = flags
        self.sequence = sequence
        self.last_ledger_sequence = last_ledger_sequence
        self.account_txn_id = account_txn_id
        self.memos = memos if memos is not None else []
        self.signers = signers if signers is not None else []
        self.source_tag = source_tag
        self.account = account
        self.signing_pub_key = signing_pub_key
        self.account_set = account_set
        self.check_cancel = check_cancel
        self.check_cash = check_cash
        self.check_create = check_create
        self.deposit_preauth = deposit_preauth
        self.escrow_cancel = escrow_cancel
        self.escrow_create = escrow_create
        self.escrow_finish = escrow_finish
        self.offer_cancel = offer_cancel
        self.offer_create = offer_create
        self.payment = payment
        self.payment_channel_claim = payment_channel_claim
        self.payment_channel_create = payment_channel_create
        self.payment_channel_fund = payment_channel_fund
        self.set_regular_key = set_regular_key
        self.signer_list_set = signer_list_set
        self.trust_set = trust_set
        self.account_delete = account_delete

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
            2: ('fee', p.UVarintType, 0),
            3: ('flags', p.UVarintType, 0),
            4: ('sequence', p.UVarintType, 0),
            5: ('last_ledger_sequence', p.UVarintType, 0),
            7: ('account_txn_id', p.UnicodeType, 0),
            8: ('memos', RippleMemo, p.FLAG_REPEATED),
            9: ('signers', RippleSigner, p.FLAG_REPEATED),
            10: ('source_tag', p.UVarintType, 0),
            11: ('account', p.UnicodeType, 0),
            12: ('signing_pub_key', p.UnicodeType, 0),
            13: ('account_set', RippleAccountSet, 0),
            14: ('check_cancel', RippleCheckCancel, 0),
            15: ('check_cash', RippleCheckCash, 0),
            16: ('check_create', RippleCheckCreate, 0),
            17: ('deposit_preauth', RippleDepositPreauth, 0),
            18: ('escrow_cancel', RippleEscrowCancel, 0),
            19: ('escrow_create', RippleEscrowCreate, 0),
            20: ('escrow_finish', RippleEscrowFinish, 0),
            21: ('offer_cancel', RippleOfferCancel, 0),
            22: ('offer_create', RippleOfferCreate, 0),
            6: ('payment', RipplePayment, 0),
            23: ('payment_channel_claim', RipplePaymentChannelClaim, 0),
            24: ('payment_channel_create', RipplePaymentChannelCreate, 0),
            25: ('payment_channel_fund', RipplePaymentChannelFund, 0),
            26: ('set_regular_key', RippleSetRegularKey, 0),
            27: ('signer_list_set', RippleSignerListSet, 0),
            28: ('trust_set', RippleTrustSet, 0),
            29: ('account_delete', RippleAccountDelete, 0),
        }
