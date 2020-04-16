from enum import Enum


class PossibleStatus(str, Enum):
    not_done = "not done"
    in_progress = "in progress"
    done = "done"
