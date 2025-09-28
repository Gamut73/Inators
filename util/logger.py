from rich import print as rprint

INFO_LABEL = "[bold blue]INFO:[/bold blue]"
WARNING_LABEL = "[bold yellow]WARNING:[/bold yellow]"
ERROR_LABEL = "[bold red]ERROR:[/bold red]"


def info(message: str):
    rprint(f"{INFO_LABEL} {message}")


def warning(message: str):
    rprint(f"{WARNING_LABEL} {message}")


def error(message: str):
    rprint(f"{ERROR_LABEL} {message}")


def debug(message: str):
    rprint(f"[bold magenta]DEBUG:[/bold magenta] {message}")


if __name__ == "__main__":
    info("This is an informational message.")
    warning("This is a warning message.")
    error("This is an error message.")
    debug("This is a debug message.")
