"""
This file contains the HTMLPage class, which is used to generate an HTML page for a directory in
the file system.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ..filesystem import Directory
from .plots.plot_generator import PlotGenerator


class HTMLPage:
    """
    Represents an HTML page for a directory in the file system.

    Attributes:
        directory (Directory): The directory for which the HTML page is to be generated.
        output_directory (Path): The directory in which the HTML page is to be saved.

    Methods:
        generate: Generates the HTML page for the directory.
        generate_pie_plot: Generates a pie plot for a column in the dataframe.
    """

    # Class Variable for storing the directory structure
    directory_structure = None

    def __init__(self, directory: Directory, output_directory: Path):
        self.directory = directory
        self.output_directory = output_directory
        self.jinja_env = Environment(
            loader=FileSystemLoader("src/sddmp/outputs/templates"), autoescape=True
        )

    @property
    def relative_path_to_root(self) -> str:
        """
        Returns the relative path from the output directory to the root directory.
        """
        num_path_parts = len(self.directory.path.parts)
        if num_path_parts == 1:
            return ".."

        return "../" * (num_path_parts)

    def generate(self) -> None:
        """
        Generates the HTML page for the directory and saves it in the output directory.
        """
        # Get the template for the html page.
        template = self.jinja_env.get_template("directory.html.j2")

        file_records_df = self.directory.file_records_dataframe()

        plot_generator = PlotGenerator(file_records_df)

        # Render the template with the dataframe.
        html = template.render(
            project_title=self.directory.metadata["ResearchProject"]["name"],
            relative_path_to_root=self.relative_path_to_root,
            directory_structure=self.directory_structure,
            my_path=self.directory.path.as_posix(),
            num_files=len(file_records_df),
            num_directories=len(self.directory.all_descendants) + 1,
            people=self.directory.metadata.get_people(),
            filetree=self.directory.filetree,
            plots={
                name: plot.as_json()
                for name, plot in plot_generator.all_plots().items()
            },
            metadata=self.directory.metadata_as_plaintext(),
            file_records_df=file_records_df,
            depth=len(self.directory.path.parts),
        )

        # Create a path to the html file.
        path = self.output_directory / self.directory.path / "index.html"

        # Create the directory for the html file if it does not exist.
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write the html file.
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
