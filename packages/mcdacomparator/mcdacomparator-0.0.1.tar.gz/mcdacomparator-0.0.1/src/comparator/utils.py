import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def plot_correlations_heatmap(
        pivot: pd.DataFrame,
        title: str = "Correlation matrix",
        font_scale: float = 0.7,
        labels_format: str = ".4f",
        color_map: str = "YlGnBu",
        x_label: str = "MCDA methods",
        y_label: str = "MCDA methods",
        figure_size: tuple = (16, 9),
):
    plt.figure(figsize=figure_size)
    sns.set(font_scale=font_scale)
    ax = sns.heatmap(pivot, annot=True, fmt=labels_format, cmap=color_map,
                     linewidth=0.5, linecolor='w')
    plt.yticks(va="center")
    plt.yticks(va="center")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()

    return plt
