# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleOfferCancel(p.MessageType):

    def __init__(
        self,
        offer_sequence: int = None,
    ) -> None:
        self.offer_sequence = offer_sequence

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('offer_sequence', p.UVarintType, 0),
        }