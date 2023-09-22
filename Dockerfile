### base stage
FROM python:3 AS base

# 作業ディレクトリを作成
WORKDIR /usr/src/jet_black_pomeranian

# 必要なファイルのみコピー
COPY src .env requirements.txt schedule.yml ./

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# 後で追加予定

# ### debug stage
# FROM base AS debug

# RUN pip install debugpy

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src/jet_black_pomeranian
# USER appuser

# # デバッグ用ポート解放
# EXPOSE 5678

# # デバッグ待機状態にする
# CMD [ "python", "-m", "debugpy", "--wait-for-client", "--listen", "5678", "jet_black_pomeranian.py" ]


### production stage
FROM base AS production

# Bot起動
CMD [ "python", "-u", "jet_black_pomeranian.py"]
