# GitHub Profile Analyzer

You have a GitHub profile. It has data. This project pulls that data,
structures it, and turns it into charts that tell the story of how
you code.

Point it at any public GitHub username and it works.

---

## What It Does

Start with a GitHub username. The program fetches your public profile,
all your repositories, and their metadata. From there it derives
language usage, repo growth over time, size distribution, and star
counts. The result is a set of charts saved to `/charts` and a clean
terminal summary.

No browser. No dashboard. Just run it and read the output.

---

## What You Need

- Python 3.12+
- A GitHub Personal Access Token
- [uv](https://docs.astral.sh/uv/) for package management

That is it.

---

## Getting Your Token

A token is how GitHub knows who is asking. Without one you are limited
to 60 API requests per hour. With one you get 5000.

1. Go to `github.com/settings/tokens`
2. Click **Generate new token (classic)**
3. Name it anything
4. Check `repo` and `read:user`
5. Generate and copy it immediately. You will not see it again.

---

## Setup

Clone the repo and move into it:

```bash
git clone https://github.com/MannyYebz/github-profile-analyzer.git
cd github-profile-analyzer
```

Install dependencies:

```bash
uv sync
```

Create a `.env` file at the project root:

GITHUB_TOKEN=your_token_here

GITHUB_USERNAME=your_github_username

Run it:

```bash
uv run main.py
```

---

## What You Get

**Terminal output:**

GITHUB PROFILE

Name         : Emmanuel Yeboah

Username     : MannyYebz

Public Repos : 20

Followers    : 2

Member Since : 2020-10-27
REPOSITORY SUMMARY

Total Repos  : 20

Original     : 17

Forks        : 3

Top Language : Python

---

## How It Works

The GitHub REST API is public and well documented. Every request goes
to `https://api.github.com` with your token in the Authorization
header. The response is JSON. We parse it into pandas DataFrames and
run the analysis from there.

Pagination is handled automatically. GitHub caps responses at 100 repos
per page. If you have more than 100 repos the fetch function handles
the extra pages without you thinking about it.

---

## Pointing It at Someone Else

Change `GITHUB_USERNAME` in your `.env` to any public GitHub username: