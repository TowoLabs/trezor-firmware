# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleAccountDelete(p.MessageType):

    def __init__(
        self,
        destination: str = None,
        destination_tag: int = None,
    ) -> None:
        self.destination = destination
        self.destination_tag = destination_tag

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('destination', p.UnicodeType, 0),
            2: ('destination_tag', p.UVarintType, 0),
        }
