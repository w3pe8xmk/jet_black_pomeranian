FROM python:3

# 作業ディレクトリを作成
WORKDIR /app

# Botアプリケーションをコピー
COPY . /app

# リストを使って依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# Bot起動
CMD [ "python", "-u", "app/jet_black_pomeranian.py"]
