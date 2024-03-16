class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_warning(message):
    print(TerminalColors.WARNING + message + TerminalColors.ENDC)


def print_error(message):
    print(TerminalColors.FAIL + message + TerminalColors.ENDC)


def print_success(message):
    print(TerminalColors.OKGREEN + message + TerminalColors.ENDC)


def print_info(message):
    print(TerminalColors.OKCYAN + message + TerminalColors.ENDC)


def print_blue(message):
    print(TerminalColors.OKBLUE + message + TerminalColors.ENDC)


def print_header(message):
    print(TerminalColors.HEADER + message + TerminalColors.ENDC)


def print_bold(message):
    print(TerminalColors.BOLD + message + TerminalColors.ENDC)


if __name__ == '__main__':
    print_warning("This is a warning message")
    print_error("This is an error message")
    print_success("This is a success message")
    print_info("This is an info message")
    print_header("This is a header message")
    print_bold("This is a bold message")
    print_blue("This is a blue message")
