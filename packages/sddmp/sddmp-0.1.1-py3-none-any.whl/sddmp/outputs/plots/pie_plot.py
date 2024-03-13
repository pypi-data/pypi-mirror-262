"""
This file contains the PiePlot class, which is used to create a pie plot using the Plotly library.
"""

import plotly.graph_objects as go

from .base_plot import BasePlot


class PiePlot(BasePlot):
    """
    Represents a pie plot using the Plotly library.

    Attributes:
        title (str): The title of the plot.
        labels (list[str]): The labels of the pie plot.
        values (list[float]): The values of the pie plot.

    Methods:
        get: Get the pie plot as a Plotly graph object figure.
    """

    def __init__(self, title, labels, values):
        super().__init__(title=title)
        self.labels = labels
        self.values = values

    def get(self) -> go.Figure:
        return super().get().add_trace(go.Pie(labels=self.labels, values=self.values))
