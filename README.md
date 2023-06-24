# jet_black_pomeranian

漆黒のポメラニアン団でお世話をしている犬。
![](./doc/img/pome.png)

# 機能

- 古戦場・ドレバラ時、色々言ってくれる
- 「ヒヒイロチャレンジ」と言えば、ヒヒイロチャレンジができる
- 「アルバハ募集」と言えば、テンプレートを置いてくれる
- 「つよ募集」と言えば、テンプレートを置いてくれる
- 「ルシ募集」と言えば、テンプレートを置いてくれる
- 「バブ募集」と言えば、テンプレートを置いてくれる
- 「ベリアル募集」と言えば、テンプレートを置いてくれる

# 実行方法

## Dockerとして実行する場合（推薦）

以下のコマンドで実行

```bash
docker build -t jet_black_pomeranian .
docker run -it --rm jet_black_pomeranian
```

## Python3がインストール済みのLinux環境で実行する場合

以下のコマンドで実行

```bash
# 必要なものをインストール
python3 -m pip install --no-cache-dir -r requirements.txt
# 必要な環境ファイルをコピー
cp schedule.yml .env ./src
# Bot実行
python3 ./src/jet_black_pomeranian.py
```

※Windowsの場合、「python3」ではなく「py3」で実行する場合もあります。
実行環境に応じて変更してください。

# 利用方法

heroku の Dyno を利用する
各環境変数を設定する
ex. `heroku config:set DISCORD_TOKEN=your_token`

# TODO

- テストコードの追加(unittest, pytest?)
- アルバハ募集
  - 6人がリアクションしたらポメラニアンが教えてくれる
  - 6人がリリアクションしたら2部の募集をかけてくれる
- google spread sheets の値を読めるようになりたい
- ルシ属性
  - ルシ募集の属性リアクションから「ルシ属性」でポメラニアンが担当の属性を考えてくれる
- ルシの行動を教えてくれるbotの作成
- 古戦場の定期発言
  - loop だと1分ごとに余計な処理が走るのでより良い方法を検討
- Discordの招待URLを教えてくれる
- 団員のtwitter救援を拾えるようにしたい
- スケジュール取り込み方法の改善
  - 現状の方法だと起動時に1回のみschedule.ymlを読み込む仕様であり、古戦場開催予定が出るたびにファイル更新して実行し直す必要がある。外部参照する形にして起動時or1日1回取り込む形にしたい
