FROM python:3

# 作業ディレクトリを作成
WORKDIR /usr/src/jet_black_pomeranian

# 必要なファイルのみコピー
COPY src .env requirements.txt schedule.yml .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# Bot起動
CMD [ "python", "-u", "jet_black_pomeranian.py"]
