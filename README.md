# update_github_img_url

GitHub でリポジトリをプライベートからパブリックに変える際に Issue などの画像 (ドラッグドロップでアップロードしたもの) の URL が無効になってしまう (プライベートに戻すと復活する) ことがある。(※)  
そのダウンロード・アップロード・書き換えを補助する Python スクリプトを作成した。

(※) **2023-12-22 現在、無効にならなくなっていそう。** (パブリック変更後も、自分も他ユーザーも画像を見ることができる)  
パブリックに変更する際の警告文からもその旨の記載が消えている。2023-11-23 時点では記載があった。

## 使い方

1. GitHub トークンを取得する。
   - GitHub の右上の自分のサムネ → Settings → Developer settings → Personal access tokens の Fine-grained tokens → Generate new token
   - 以下の 4 個の権限を付与する。
     - Contents: Read-only
     - Metadata: Read-only
     - Issues: Read and write
     - Pull requests: Read and write
1. このリポジトリをクローンする。
1. `pip install -r requirements.txt`
1. `python step1.py [GitHubユーザー名/リポジトリ名] [トークン]` → 画像 URL が取得される
1. 出力された URL の画像を手動ですべてダウンロード、デフォルト名のまま保存
1. Settings からリポジトリをプライベート → パブリックに変える
1. Issue を新規作成するページに行き、テキストボックスに全画像をドラッグドロップしてアップロード
1. テキストボックスの全内容を、クローンしたリポジトリに `new_url_map.txt` として保存
   - サンプルファイル `new_url_map_sample.txt` と同じような形式であることを確認
1. `python step2.py [GitHubユーザー名/リポジトリ名] [トークン]` → 画像 URL が書き換わる
1. 対象リポジトリの `README.md` の中身の画像 URL は `step1.py` で取得されるが、`step2.py` での書き換えは行われない。もし存在するなら、手動で書き換えてコミットする必要あり。

## ライセンス

MIT License

## 関連リンク

- 作成者 X (Twitter): https://twitter.com/Tomii9273
