import argparse
import sys
from importlib.metadata import version
from . import module


def main():
    """
    Entry point for the prompit CLI tool.
    Parses command line arguments and calls the appropriate functions.
    """
    current_version = version("prompit")

    parser = argparse.ArgumentParser(
        prog="prompit", description="CLI tool to promptify entire codebases."
    )
    parser.add_argument(
        "-i",
        "--ignore",
        nargs="*",
        default=[],
        help="Additional specs and files to ignore",
    )
    parser.add_argument(
        "-a",
        "--append",
        nargs="*",
        default=[],
        help="Files and specs to include on the final prompt",
    )
    parser.add_argument(
        "-m", "--message", help="Append an instruction message on prompt."
    )
    parser.add_argument(
        "-g",
        "--greeting",
        default="Great, so we have this:",
        help="Change the prefixed context. Defaults to 'Great, so we have this:'",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {current_version}",
        help="Show installed version",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all files matching the current specs",
    )
    parser.add_argument(
        "-s",
        "--structure",
        action="store_true",
        help="Print the directory structure",
    )
    parser.add_argument(
        "-x",
        "--no-xml",
        action="store_false",
        help="If present, it will not wrap each file with '<!-- file -->' and '<!-- end of file -->'",
    )

    args = parser.parse_args()

    if args.list:
        filepaths = module.list_files(
            include_files=args.append, ignore_files=args.ignore
        )
        print(f"{len(filepaths)} selected files\n")
        print(module.get_repo_structure(filepaths=filepaths))

        command = " ".join(arg for arg in sys.argv[1:] if arg not in ["-l", "--list"])
        print("\nRun `prompit" + (f" {command}`" if command else "") + "`")
    else:
        print(f"{args.greeting}\n\n")
        promptified_repo = module.get_promptified_repo(
            include_files=args.append,
            ignore_files=args.ignore,
            show_structure=args.structure,
            xml_comments=args.no_xml,
        )
        print(promptified_repo)

        if args.message:
            print(f"\n\n{args.message}")
