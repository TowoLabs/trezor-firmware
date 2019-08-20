# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleSignerEntry(p.MessageType):

    def __init__(
        self,
        account: str = None,
        signer_weight: int = None,
    ) -> None:
        self.account = account
        self.signer_weight = signer_weight

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('account', p.UnicodeType, 0),
            2: ('signer_weight', p.UVarintType, 0),
        }
