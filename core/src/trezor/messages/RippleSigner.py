# Automatically generated by pb2py
# fmt: off
import protobuf as p

from .RippleInternalSigner import RippleInternalSigner

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleSigner(p.MessageType):

    def __init__(
        self,
        signer: RippleInternalSigner = None,
    ) -> None:
        self.signer = signer

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('signer', RippleInternalSigner, 0),
        }
