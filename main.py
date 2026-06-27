from src.github_analyzer.fetch_github import (
    get_user_profile,
    get_repos,
    get_language_stats,
    print_repo_summary,
)
from src.github_analyzer.analyze_github import (
    plot_language_distribution,
    plot_repos_over_time,
    plot_repo_types,
    plot_top_repos_by_size,
    plot_top_repos_by_stars,
)


def main():
    print()
    print("  GITHUB PROFILE ANALYZER")
    print("  ========================")

    get_user_profile()

    df = get_repos()
    print_repo_summary(df)
    lang_df = get_language_stats(df)

    print("  Generating charts...")
    print()

    plot_language_distribution(lang_df)
    plot_repos_over_time(df)
    plot_repo_types(df)
    plot_top_repos_by_size(df)
    plot_top_repos_by_stars(df)

    print()
    print("  Done. Charts saved to /charts")


if __name__ == "__main__":
    main()