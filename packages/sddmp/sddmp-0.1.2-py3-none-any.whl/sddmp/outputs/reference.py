"""
This file contains the Reference class, which is used to generate an HTML page for the glossary of
terms and special keys used in the project.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class Reference:
    # Class Variable for storing the directory structure
    directory_structure = None

    def __init__(self, input_directory: Path, output_directory: Path):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.jinja_env = Environment(
            loader=FileSystemLoader("src/sddmp/outputs/templates"), autoescape=True
        )

    def generate(self) -> None:
        # Get the template for the html page.
        template = self.jinja_env.get_template("reference.html.j2")

        html = template.render(
            directory_structure=self.directory_structure,
            relative_path_to_root="..",
            depth=0,
        )

        # Create a path to the html file.
        path = (
            Path(self.output_directory) / Path(self.input_directory) / "reference.html"
        )

        # Create the directory for the html file if it does not exist.
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write the html file.
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
