import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
from fetch_github import get_user_profile, get_repos, get_language_stats

os.makedirs("charts", exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "#0d0d0d",
    "axes.facecolor": "#0d0d0d",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#cccccc",
    "xtick.color": "#888888",
    "ytick.color": "#888888",
    "text.color": "#cccccc",
    "grid.color": "#1a1a1a",
    "grid.linestyle": "--",
    "font.family": "monospace",
})

ACCENT = "#ffffff"
SPOTIFY_GREEN = "#1DB954"
COLORS = [
    "#1DB954", "#FF6B6B", "#4ECDC4", "#FFE66D",
    "#A8E6CF", "#FF8B94", "#C7CEEA", "#F7B731", "#778CA3"
]
FIG_SIZE = (10, 5)


def plot_language_distribution(lang_df):
    if lang_df is None or lang_df.empty:
        print("  No language data.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#0d0d0d")

    colors = COLORS[:len(lang_df)]
    wedges, texts, autotexts = ax.pie(
        lang_df["repo_count"],
        labels=lang_df["language"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        pctdistance=0.82,
    )

    for text in texts:
        text.set_fontsize(11)
        text.set_color("#cccccc")
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    ax.set_title("Language Distribution", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=20)

    plt.tight_layout()
    plt.savefig("charts/language_distribution.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/language_distribution.png")
    plt.show()


def plot_repos_over_time(df):
    if df is None or df.empty:
        print("  No repo data.")
        return

    df = df.copy()
    df["year_month"] = df["created_at"].dt.to_period("M")
    monthly = df.groupby("year_month").size().reset_index(name="count")
    monthly["year_month"] = monthly["year_month"].dt.to_timestamp()
    monthly["cumulative"] = monthly["count"].cumsum()

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    fig.patch.set_facecolor("#0d0d0d")

    ax.fill_between(monthly["year_month"], monthly["cumulative"],
                    color=SPOTIFY_GREEN, alpha=0.3)
    ax.plot(monthly["year_month"], monthly["cumulative"],
            color=SPOTIFY_GREEN, linewidth=2, marker="o", markersize=4)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30, ha="right", fontsize=8)

    ax.set_ylabel("Total Repositories", fontsize=10)
    ax.set_title("Repository Growth Over Time", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True)

    plt.tight_layout()
    plt.savefig("charts/repos_over_time.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/repos_over_time.png")
    plt.show()


def plot_repo_types(df):
    if df is None or df.empty:
        print("  No repo data.")
        return

    original = len(df[df["is_fork"] == False])
    forked = len(df[df["is_fork"] == True])

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor("#0d0d0d")

    wedges, texts, autotexts = ax.pie(
        [original, forked],
        labels=["Original", "Forked"],
        autopct="%1.1f%%",
        colors=[SPOTIFY_GREEN, "#FF6B6B"],
        startangle=90,
        pctdistance=0.82,
    )

    for text in texts:
        text.set_fontsize(11)
        text.set_color("#cccccc")
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    ax.set_title("Original vs Forked Repos", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=20)

    plt.tight_layout()
    plt.savefig("charts/repo_types.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/repo_types.png")
    plt.show()


def plot_top_repos_by_size(df):
    if df is None or df.empty:
        print("  No repo data.")
        return

    df_plot = df[df["size_kb"] > 0].nlargest(10, "size_kb").iloc[::-1]

    n = len(df_plot)
    fig_height = max(4, n * 0.6)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    fig.patch.set_facecolor("#0d0d0d")

    colors = [SPOTIFY_GREEN] * n
    colors[-1] = "#ffffff"

    bars = ax.barh(
        df_plot["name"],
        df_plot["size_kb"],
        color=colors,
        edgecolor="none",
        height=0.4,
    )

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)} KB",
            va="center", fontsize=9, color="#888888",
        )

    ax.set_title("Top Repos by Size", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", labelsize=10)

    plt.tight_layout()
    plt.savefig("charts/top_repos_by_size.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/top_repos_by_size.png")
    plt.show()


def plot_top_repos_by_stars(df):
    if df is None or df.empty:
        print("  No repo data.")
        return

    df_stars = df[df["stars"] > 0].nlargest(10, "stars").iloc[::-1]

    if df_stars.empty:
        print("  Stars chart: no starred repos yet.")
        return

    n = len(df_stars)
    fig_height = max(4, n * 0.6)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    fig.patch.set_facecolor("#0d0d0d")

    colors = ["#FFE66D"] * n
    colors[-1] = "#ffffff"

    bars = ax.barh(
        df_stars["name"],
        df_stars["stars"],
        color=colors,
        edgecolor="none",
        height=0.4,
    )

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)} ★",
            va="center", fontsize=9, color="#888888",
        )

    ax.set_title("Top Repos by Stars", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", labelsize=10)

    plt.tight_layout()
    plt.savefig("charts/top_repos_by_stars.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/top_repos_by_stars.png")
    plt.show()


if __name__ == "__main__":
    print()
    print("  GITHUB PROFILE ANALYSIS")
    print("  ========================")
    print()

    get_user_profile()

    print("  Fetching repositories...")
    df = get_repos()
    lang_df = get_language_stats(df)

    print()
    print("  Generating charts...")
    print()

    plot_language_distribution(lang_df)
    plot_repos_over_time(df)
    plot_repo_types(df)
    plot_top_repos_by_size(df)
    plot_top_repos_by_stars(df)

    print()
    print("  Done. Charts saved to /charts")