# 使い方

1. リポジトリをクローンしてください．
2. Docker Desktop のインストールをする．
3. プロジェクトのルート直下で`docker compose build`でビルドを行う．
4. 同様に`docker compose up -d`で起動．
5. 同様に`docker exec -it sb-api-python3 /bin/bash `でコンテナの中に入る．
6. `cd app`で app ディレクトリに移動．
7. app ディレクトリの中に`.env`ファイルを作成．
8. `.env`ファイルに以下を記述する．=の後に必要な記述をする．

```
SB_TOKEN=
SECRET_TOKEN=

# :を削除してください
DEVICE_ID=
```

9. `python3 ファイル名`でプログラムを実行．
10. 終了時は`exit`でコンテナから抜け，`docker compose down`でコンテナを終了させる．
