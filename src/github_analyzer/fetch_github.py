import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")
BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_user_profile():
    url = f"{BASE_URL}/users/{USERNAME}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json().get('message')}")
        return None

    data = response.json()

    print()
    print("=" * 55)
    print("  GITHUB PROFILE")
    print("=" * 55)
    print(f"  Name        : {data.get('name', 'N/A')}")
    print(f"  Username    : {data.get('login')}")
    print(f"  Bio         : {data.get('bio', 'N/A')}")
    print(f"  Location    : {data.get('location', 'N/A')}")
    print(f"  Public Repos: {data.get('public_repos', 0)}")
    print(f"  Followers   : {data.get('followers', 0)}")
    print(f"  Following   : {data.get('following', 0)}")
    print(f"  Member Since: {data.get('created_at', '')[:10]}")
    print()

    return data


def get_repos(per_page=100):
    """
    GitHub paginates responses at 30 by default, max 100 per page.
    We fetch up to 100 repos in one call.
    This teaches you about pagination parameters.
    """
    url = f"{BASE_URL}/users/{USERNAME}/repos"
    params = {
        "per_page": per_page,
        "sort": "updated",
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json().get('message')}")
        return None

    data = response.json()

    repos = []
    for repo in data:
        repos.append({
            "name": repo.get("name"),
            "description": repo.get("description", ""),
            "language": repo.get("language", "Unknown"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "size_kb": repo.get("size", 0),
            "created_at": repo.get("created_at", "")[:10],
            "updated_at": repo.get("updated_at", "")[:10],
            "is_fork": repo.get("fork", False),
            "topics": ", ".join(repo.get("topics", [])),
            "url": repo.get("html_url", ""),
        })

    df = pd.DataFrame(repos)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])

    return df


def get_language_stats(df):
    """
    Derive language usage from repos.
    Count how many repos use each language.
    """
    lang_counts = (
        df[df["language"] != "Unknown"]["language"]
        .value_counts()
        .reset_index()
    )
    lang_counts.columns = ["language", "repo_count"]
    return lang_counts


def print_repo_summary(df):
    print("=" * 55)
    print("  REPOSITORY SUMMARY")
    print("=" * 55)

    original = df[df["is_fork"] == False]
    forks = df[df["is_fork"] == True]

    print(f"  Total Repos   : {len(df)}")
    print(f"  Original      : {len(original)}")
    print(f"  Forks         : {len(forks)}")
    print(f"  Total Stars   : {df['stars'].sum()}")
    print(f"  Most Starred  : {df.loc[df['stars'].idxmax(), 'name']} ({df['stars'].max()} stars)")
    print(f"  Top Language  : {df['language'].value_counts().index[0]}")
    print()

    print("  Top 10 Repos by Stars:")
    print(f"  {'Repo':<35} {'Stars':>6} {'Language':<15}")
    print("  " + "-" * 55)
    for _, row in df.nlargest(10, "stars").iterrows():
        print(f"  {row['name']:<35} {row['stars']:>6} {str(row['language']):<15}")
    print()


if __name__ == "__main__":
    get_user_profile()

    print("  Fetching repositories...")
    df = get_repos()

    if df is not None:
        print(f"  Loaded {len(df)} repositories")
        print()
        print_repo_summary(df)

        lang_stats = get_language_stats(df)
        print("=" * 55)
        print("  LANGUAGE BREAKDOWN")
        print("=" * 55)
        for _, row in lang_stats.iterrows():
            bar = "█" * row["repo_count"]
            print(f"  {row['language']:<20} {bar} ({row['repo_count']})")
        print()