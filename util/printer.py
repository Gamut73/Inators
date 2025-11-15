from dataclasses import dataclass

from rich.console import Console
from rich.table import Table


@dataclass
class TableColumn:
    name: str
    style: str = "dim"
    width: int = 20


@dataclass
class TableConfig:
    show_header: bool = True
    header_style: str = "bold magenta"
    show_lines: bool = True


@dataclass
class TableData:
    columns: list['TableColumn']
    rows: list[list[str]]
    title: str = ""
    config: TableConfig = TableConfig()


def print_table(data: TableData):
    console = Console()

    table_config = data.config
    table = Table(
        title=data.title,
        show_header=False if not data.title else table_config.show_header,
        header_style=table_config.header_style,
        show_lines=table_config.show_lines
    )
    for column in data.columns:
        table.add_column(column.name, style=column.style, width=column.width)

    for row in data.rows:
        table.add_row(*map(str, row))

    console.print(table)


if __name__ == "__main__":
    columns = [
        TableColumn(name="Name", style="cyan", width=20),
        TableColumn(name="Age", style="green", width=10),
        TableColumn(name="City", style="magenta", width=15)
    ]

    rows = [
        ["Alice", "30", "New York"],
        ["Bob", "25", "Los Angeles"],
        ["Charlie", "35", "Chicago"]
    ]

    test_data = TableData(columns=columns, rows=rows, title="User Information")

    print_table(test_data)
