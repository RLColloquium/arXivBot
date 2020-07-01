# arXivBot

Slack で arXiv の URL を書くとタイトルやアブストラクト等を通知するボット

![image](https://user-images.githubusercontent.com/1632335/86212298-bbf21a00-bbb2-11ea-912f-1a152fede6ad.png)


## 実装と設定

Heroku アカウントの作成から heroku login までを以下のページを参考に済ませておきます. このチュートリアルは Web アプリの例なので, 今回はあまり参考にならないかもです. 今回のは worker というタイプのアプリです.

https://devcenter.heroku.com/articles/getting-started-with-python

それ以降は, 基本的には以下のページ通りに実装して Heroku にデププロイします.

https://qiita.com/akabei/items/ec5179794f9e4e1df203#slack-bot%E4%BD%9C%E6%88%90

ただし, `slackbot_settings.py` の API Token はソースコード中には書かずに,

```Python
API_TOKEN = '<API Token>'
```

以下のように環境変数 SLACK_API_TOKEN で設定しておきます.

```Python
import os

API_TOKEN = os.environ['SLACK_API_TOKEN']
```

Heroku での環境変数の設定方法は以下のページを参照.

https://devcenter.heroku.com/articles/config-vars

CLI のコマンドか Web で設定できますが, CLI だとシェルのヒストリに残ってしまうので Web で設定した方が良いかもしれません.

ローカルで実験する時は ~/.zshrc に書いておきます.

```sh
SLACK_API_TOKEN="xxxxx"
```

上記記事中の my_slackbot.py は任意のファイル名で OK です.


## 開発サイクル

今の所, 以下のようなサイクルで開発しています.

```sh
(コードを変更)
python run.py # ローカルでテスト
(Slack で動作確認)
git add
git commit
git push heroku master # Heroku にアップロードされてコードが更新
(Slack で動作確認)
```
