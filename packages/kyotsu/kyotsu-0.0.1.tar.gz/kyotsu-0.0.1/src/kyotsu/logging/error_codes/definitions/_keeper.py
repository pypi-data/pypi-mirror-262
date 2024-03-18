__all__ = [
    "ErrorCodesKeeper",
]

from typing import Final

from kyotsu.logging.error_codes.dataclasses import error_code_keeper

from .kyotsu import KyotsuKeeper
from .scheduler_service import SchedulerKeeper
from .uncategorized import UncategorizedKeeper


@error_code_keeper
class ErrorCodesKeeper:
    """
    A single keeper for all error codes.
    Instance of this class serves as an entrypoint to the :sparkles:error codes world:sparkles:.


    To introduce a new category simply add new class attribute with
    Prefix as attribute name, `Final[<your_keeper_class>]` as attribute type,
    and your keeper class instance as attribute value.

    Attributes:
        UN: Keeps uncategorized error codes.
        KTS: Keeps kyotsu runtime error codes.
    """

    UN: Final[UncategorizedKeeper] = UncategorizedKeeper()
    KTS: Final[KyotsuKeeper] = KyotsuKeeper()
    SCH: Final[SchedulerKeeper] = SchedulerKeeper()
