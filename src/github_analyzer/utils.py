import matplotlib.pyplot as plt
import os

# Shared constants
ACCENT = "#ffffff"
GREEN = "#1DB954"
RED = "#FF6B6B"
TEAL = "#4ECDC4"
YELLOW = "#FFE66D"
GRAY = "#888888"
DARK_BG = "#0d0d0d"

COLORS = [GREEN, RED, TEAL, YELLOW, "#A8E6CF", "#FF8B94", "#C7CEEA", "#F7B731", "#778CA3"]

FIG_SIZE = (10, 5)


def set_dark_theme():
    plt.rcParams.update({
        "figure.facecolor": DARK_BG,
        "axes.facecolor": DARK_BG,
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#cccccc",
        "xtick.color": GRAY,
        "ytick.color": GRAY,
        "text.color": "#cccccc",
        "grid.color": "#1a1a1a",
        "grid.linestyle": "--",
        "font.family": "monospace",
        "figure.dpi": 100,
    })


def save_chart(filename):
    os.makedirs("charts", exist_ok=True)
    plt.tight_layout()
    plt.savefig(f"charts/{filename}", dpi=150,
                bbox_inches="tight", facecolor=DARK_BG)
    print(f"  Saved: charts/{filename}")
    plt.show()


def clean_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)