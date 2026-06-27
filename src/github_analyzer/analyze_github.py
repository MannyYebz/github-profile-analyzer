import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from .utils import (
    set_dark_theme, save_chart, clean_axes,
    ACCENT, GREEN, RED, YELLOW, GRAY, COLORS, FIG_SIZE, DARK_BG
)

set_dark_theme()


def plot_language_distribution(lang_df):
    if lang_df is None or lang_df.empty:
        print("  No language data.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(DARK_BG)

    wedges, texts, autotexts = ax.pie(
        lang_df["repo_count"],
        labels=lang_df["language"],
        autopct="%1.1f%%",
        colors=COLORS[:len(lang_df)],
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

    save_chart("language_distribution.png")


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
    fig.patch.set_facecolor(DARK_BG)

    ax.fill_between(monthly["year_month"], monthly["cumulative"],
                    color=GREEN, alpha=0.3)
    ax.plot(monthly["year_month"], monthly["cumulative"],
            color=GREEN, linewidth=2, marker="o", markersize=4)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Total Repositories", fontsize=10)
    ax.set_title("Repository Growth Over Time", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=15)
    clean_axes(ax)
    ax.yaxis.grid(True)

    save_chart("repos_over_time.png")


def plot_repo_types(df):
    if df is None or df.empty:
        print("  No repo data.")
        return

    original = len(df[df["is_fork"] == False])
    forked = len(df[df["is_fork"] == True])

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(DARK_BG)

    wedges, texts, autotexts = ax.pie(
        [original, forked],
        labels=["Original", "Forked"],
        autopct="%1.1f%%",
        colors=[GREEN, RED],
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

    save_chart("repo_types.png")


def plot_top_repos_by_size(df):
    if df is None or df.empty:
        print("  No repo data.")
        return

    df_plot = df[df["size_kb"] > 0].nlargest(10, "size_kb").iloc[::-1]
    n = len(df_plot)

    fig, ax = plt.subplots(figsize=(10, max(4, n * 0.6)))
    fig.patch.set_facecolor(DARK_BG)

    colors = [GREEN] * n
    colors[-1] = "#ffffff"

    bars = ax.barh(df_plot["name"], df_plot["size_kb"],
                   color=colors, edgecolor="none", height=0.4)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height() / 2,
                f"{int(width)} KB", va="center", fontsize=9, color=GRAY)

    ax.set_title("Top Repos by Size", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=15)
    clean_axes(ax)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", labelsize=10)

    save_chart("top_repos_by_size.png")


def plot_top_repos_by_stars(df):
    if df is None or df.empty:
        print("  No repo data.")
        return

    df_stars = df[df["stars"] > 0].nlargest(10, "stars").iloc[::-1]

    if df_stars.empty:
        print("  Stars chart: no starred repos yet.")
        return

    n = len(df_stars)
    fig, ax = plt.subplots(figsize=(10, max(4, n * 0.6)))
    fig.patch.set_facecolor(DARK_BG)

    colors = [YELLOW] * n
    colors[-1] = "#ffffff"

    bars = ax.barh(df_stars["name"], df_stars["stars"],
                   color=colors, edgecolor="none", height=0.4)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{int(width)} ★", va="center", fontsize=9, color=GRAY)

    ax.set_title("Top Repos by Stars", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=15)
    clean_axes(ax)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", labelsize=10)

    save_chart("top_repos_by_stars.png")