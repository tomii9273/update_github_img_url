# リポジトリの Issue・PR に書かれた画像 URL を、`new_url_map.txt` に対応するものに書き換える。
# python step2.py [GitHubユーザー名/リポジトリ名] [トークン]

from github import Github
import sys
import re
from github import Issue, IssueComment, PullRequest, PullRequestComment


# 設定
REPO_NAME = sys.argv[1]
TOKEN = sys.argv[2]


# 初期化
g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)


with open("new_url_map.txt") as f:
    new_url_map = {}
    for line in f:
        old_url = line[12:48]
        new_url = line[-38:-2]
        assert re.fullmatch(
            r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}", old_url
        )
        assert re.fullmatch(
            r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}", new_url
        )
        new_url_map[old_url] = new_url

print(new_url_map)


def edit(
    comment: Issue.Issue
    | IssueComment.IssueComment
    | PullRequest.PullRequest
    | PullRequestComment.PullRequestComment,
) -> None:
    """Issue や PR のコメント (ヘッダー含む) の画像 URL を新しいものに書き換える"""
    new_body = comment.body
    if new_body is None:
        return
    for old_url, new_url in new_url_map.items():
        new_body = new_body.replace(old_url, new_url)
    comment.edit(body=new_body)


# Issue 書き換え
for issue in repo.get_issues(state="all"):
    # print(issue.number, issue.title)
    edit(issue)
    for comment in issue.get_comments():
        edit(comment)
print("Issue done")

# PR 書き換え
for pr in repo.get_pulls(state="all"):
    # print(pr.number, pr.title)
    edit(pr)
    for comment in pr.get_issue_comments():
        edit(comment)
print("PR done")
