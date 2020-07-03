# arXivBot

[Slack](https://slack.com/) で [arXiv](https://arxiv.org/) の URL を書くとタイトルやアブストラクト等を通知するボット

[DeepL API](https://www.deepl.com/docs-api/introduction/) での翻訳にも対応しています.

![image](https://user-images.githubusercontent.com/1632335/86489762-53689000-bda0-11ea-89aa-42ddf6e2e797.png)


## 設定方法

ここでは [Heroku](https://www.heroku.com/) で arXivBot をホスティングする方法を説明します.


### Slack Bots アプリを追加

以下のページを参考に Slack の Bots アプリを作成して API Token をメモしておきます.

https://qiita.com/akabei/items/ec5179794f9e4e1df203#slack-bot%E4%BD%9C%E6%88%90


### Slack Bots アプリの招待

作った Slack Bots アプリをテスト用の Slack チャンネルに招待しておきます.

例: ボットの名前を arXiv にした場合, 招待したいチャンネルで,

```
/invite @arXiv
```


### ローカルの環境変数の設定

上記でメモした Slack Bots の API Token を環境変数 `SLACKBOT_API_TOKEN` で設定しておきます.

ローカルでテストする場合は, 環境変数を ~/.zshrc に書いておきます.

```sh
export SLACKBOT_API_TOKEN="xxxxx"
```

DeepL API を使う場合は, 同様に `DEEPL_AUTH_KEY` も設定しておきます.


### ローカル環境の設定

ローカル環境の設定と動作確認を以下のようにします.

```sh
git clone git@github.com:RLColloquium/arXivBot.git
cd arXivBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py  # ローカルで動くかテスト
# Slack で動作確認
```


### Heroku アカウントの作成と CLI のインストール

以下のチュートリアルを参考に, Heroku アカウントの作成から CLI のインストールまで済ませておきます(Postgres をインストールする必要はありません). このチュートリアルは web アプリの例なので, 今回はあまり参考にならないかもです. このアプリは worker という種類のアプリです.

https://devcenter.heroku.com/articles/getting-started-with-python


### Heroku 環境の設定

Heroku のアプリ作成を以下のようにします.

```sh
heroku login
heroku create rl-colloquium-arxivbot  # 任意のアプリ名を指定.
git remote -v  # heroku が追加されているか確認
```

Heroku へのデプロイは以下のようにします.

```sh
git push heroku master  # Heroku にコードをアップロード
```

### Heroku の環境変数の設定

以前メモした Slack Bots の API Token を環境変数 `SLACKBOT_API_TOKEN` で設定しておきます.

以下ページを参考に, Heroku 側での環境変数を設定します.

https://devcenter.heroku.com/articles/config-vars

CLI のコマンドか Web で設定できますが, CLI だとシェルのヒストリに残ってしまうので Web で設定した方が良いかもしれません.

https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard

DeepL API を使う場合は, 同様に `DEEPL_AUTH_KEY` も設定しておきます.


### Heroku アプリの起動

以下ページを参考に, Heroku アプリを起動します.

https://qiita.com/akabei/items/ec5179794f9e4e1df203#%E8%B5%B7%E5%8B%95


### Heroku のログを確認

別ターミナルを開いて, ログを確認しておきます.

```
heroku logs --tail
```


## 開発サイクル

以下のようなサイクルで開発しています.

```sh
# コードを変更
python run.py # ローカルでテスト
# Slack で動作確認
git add
git commit
git push heroku master # Heroku にアップロードされてコードが更新
# Slack で動作確認
```

## 参考

- https://devcenter.heroku.com/articles/getting-started-with-python
- https://api.slack.com/bot-users
- https://www.deepl.com/docs-api/introduction/
- https://qiita.com/akabei/items/ec5179794f9e4e1df203
- https://qiita.com/seratch/items/a001985ee1dccaf95727
