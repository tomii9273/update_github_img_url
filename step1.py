# リポジトリの Issue・PR・README.md のすべてから、GitHub にアップロードされた画像の URL を取得する
# python step1.py [GitHubユーザー名/リポジトリ名] [トークン]

from typing import Optional
from github import Github
import sys
import re

# 設定
REPO_NAME = sys.argv[1]
TOKEN = sys.argv[2]


# 初期化
g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)


def download_images_from_comment(comment_body: Optional[str]) -> set[str]:
    """Issue や PR のコメント (ヘッダー含む) の画像 URL をすべて取得する"""
    if comment_body is None:
        return set()

    pattern = rf"https://github\.com/{REPO_NAME}/assets[^)]*\)"
    urls = re.findall(pattern, comment_body)

    urls = [url[:-1] for url in urls]  # 末尾の `)` を削除

    return set(urls)


urls = set()

# Issue から
for issue in repo.get_issues(state="all"):
    # print(issue.number, issue.title)
    urls |= download_images_from_comment(issue.body)
    for comment in issue.get_comments():
        urls |= download_images_from_comment(comment.body)

# PR から（PR も Issue として扱われるので、重複する可能性がある）
for pr in repo.get_pulls(state="all"):
    # print(pr.number, pr.title)
    urls |= download_images_from_comment(pr.body)
    for comment in pr.get_issue_comments():
        urls |= download_images_from_comment(comment.body)

# README から
readme_content = repo.get_contents("README.md")
readme_data = readme_content.decoded_content.decode("utf-8")
urls |= download_images_from_comment(readme_data)

# 保存・出力
print(f"{len(urls)} URLs found")
with open("url_list.txt", "w") as f:
    for url in urls:
        f.write(url + "\n")
        print(url)
