import argparse
import logging
from pathlib import Path
import shutil

logger = logging.getLogger(__name__)


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Create a demonstration project directory structure for testing."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="example_project",
        help="The output directory to create and write the demonstration project to.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help=(
            "A Text file containing a directory structure to build the demonstration project "
            "from."
        ),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output.",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Print the output without writing to the file system.",
    )
    return parser.parse_args()


def create_directory_structure(base_path, structure, dry_run=False):
    lines = structure.split("\n")
    path_stack = []
    for line in lines:
        if line.strip() == "":
            continue
        depth = line.index(line.lstrip()) // 3
        name = line.lstrip()
        while len(path_stack) > depth:
            path_stack.pop()
        path_stack.append(name)
        path = Path(base_path, *path_stack)
        log_func = logger.info if dry_run else logger.debug
        log_func(f"Creating {path}")
        if not dry_run:
            path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    args = _parse_cli()

    # Set up logging.
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    print(f"Creating example project at {args.output}")

    if args.input:
        print(f"Using input file {args.input}")
        structure = open(args.input).read()
    else:
        print(
            "Please paste a directory structure into the terminal here (Press Enter to finish):"
        )
        structure = ""
        while True:
            text = input()
            if text == "":
                break
            structure += text + "\n"

    # Let the user see the structure that will be created.
    print("The following directory structure will be created:")
    print(structure)
    if input("Is this correct? (y/n): ").lower() != "y":
        print("Exiting.")
        exit()

    create_directory_structure(args.output, structure, args.dry_run)

    if not args.dry_run:
        # Drop a copy of the example README in the output directory.
        readme = Path(__file__).parent / "resources/README_example.yaml"
        readme_path = Path(args.output, "README.yaml")
        shutil.copy(readme, readme_path)

    print("Done!")
