from ert.enum_shim import StrEnum


class ForwardModelKeys(StrEnum):
    NAME = "NAME"
    EXECUTABLE = "EXECUTABLE"

    STDIN = "STDIN"
    STDOUT = "STDOUT"
    STDERR = "STDERR"

    START_FILE = "START_FILE"
    TARGET_FILE = "TARGET_FILE"
    ERROR_FILE = "ERROR_FILE"

    MAX_RUNNING = "MAX_RUNNING"
    MAX_RUNNING_MINUTES = "MAX_RUNNING_MINUTES"

    MIN_ARG = "MIN_ARG"
    MAX_ARG = "MAX_ARG"
    ARGLIST = "ARGLIST"
    ARG_TYPE = "ARG_TYPE"

    REQUIRED = "REQUIRED"

    ENV = "ENV"
    EXEC_ENV = "EXEC_ENV"
    DEFAULT = "DEFAULT"
    PRIVATE_ARGS = "PRIVATE_ARGS"
    HELP_TEXT = "HELP_TEXT"
