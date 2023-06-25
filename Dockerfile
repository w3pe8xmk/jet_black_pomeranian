FROM python:3

# 作業ディレクトリを作成
WORKDIR /usr/src/jet_black_pomeranian

# インストールが必要なリストをコンテナにコピー
COPY requirements.txt ./

# コピーしたリストを使って依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# Botアプリケーションをコピー
COPY src .

# 必要な環境情報をコピー
COPY schedule.yml .env .

# Bot起動
CMD [ "python", "-u", "jet_black_pomeranian.py"]
