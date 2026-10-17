import argparse

from notinspec import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="notinspec")
    parser.add_argument("--version", action="version", version=f"notinspec {__version__}")
    parser.parse_args(argv)
    parser.print_help()
    return 0
