class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALICS = '\033[3m'

    @staticmethod
    def apply_header(text):
        return f"{PrintColors.HEADER}{text}{PrintColors.ENDC}"

    @staticmethod
    def apply_okblue(text):
        return f"{PrintColors.OKBLUE}{text}{PrintColors.ENDC}"

    @staticmethod
    def apply_okgreen(text):
        return f"{PrintColors.OKGREEN}{text}{PrintColors.ENDC}"

    @staticmethod
    def apply_warning(text):
        return f"{PrintColors.WARNING}{text}{PrintColors.ENDC}"

    @staticmethod
    def apply_fail(text):
        return f"{PrintColors.FAIL}{text}{PrintColors.ENDC}"

    @staticmethod
    def apply_bold(text):
        return f"{PrintColors.BOLD}{text}{PrintColors.ENDC}"

    @staticmethod
    def apply_underline(text):
        return f"{PrintColors.UNDERLINE}{text}{PrintColors.ENDC}"

    @staticmethod
    def apply_italics(text):
        return f"{PrintColors.ITALICS}{text}{PrintColors.ENDC}"