# jet_black_pomeranian
漆黒のポメラニアン団でお世話をしている犬。  
![](./doc/img/pome.png)

# 機能
- 古戦場時、色々言ってくれる
- 「ヒヒイロチャレンジ」と言えば、ヒヒイロチャレンジができる
- 「ルシ募集」と言えば、テンプレートを置いてくれる
- 土曜以外毎日アルバハHLの募集を投げてくれる
- 土曜にルシHARDの募集を投げてくれる

# 実行方法
以下のコマンドで実行
```
pip install pyyaml
python3 jet_black_pomeranian.py
```

# 利用方法
heroku の Dyno を利用する  
各環境変数を設定する  
ex. `heroku config:set DISCORD_TOKEN=your_token`

# TODO
- Docker化(環境変数のため)
- テストコードの追加(unittest, pytest?)
- アルバハ募集 6人がリアクションしたらポメラニアンが教えてくれる
- google spread sheets の値を読めるようになりたい
- ルシ属性
    - ルシ募集の属性リアクションから「ルシ属性」でポメラニアンが担当の属性を考えてくれる
- ルシの行動を教えてくれるbotの作成
- 古戦場の定期発言
    - loop だと1分ごとに余計な処理が走るのでより良い方法を検討
    - 古戦場の日程を別ファイルに置いておく->よりよくする
- Discordの招待URLを教えてくれる
- シートのURLを教えてくれる