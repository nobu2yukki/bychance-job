# bychance-job

## 開発環境のセットアップ

### Dev Containerを使用した開発

このプロジェクトは、Frontend（Next.js/Bun）とBackend（FastAPI/Python）それぞれに専用のDev Container設定を用意しています。

#### 必要なもの

- Docker Desktop
- Visual Studio Code
- Dev Containers拡張機能

#### セットアップ手順

1. **リポジトリをクローン**
   ```bash
   git clone [repository-url]
   cd bychance-job
   ```

2. **開発したいサービスを選択**

   **Frontend開発の場合：**
   ```bash
   code frontend
   ```

   **Backend開発の場合：**
   ```bash
   code backend
   ```

3. **Dev Containerで開く**
   - VS Codeが開いたら、右下に「Reopen in Container」の通知が表示されますので、クリック
   - または、コマンドパレット（Cmd/Ctrl + Shift + P）で「Dev Containers: Reopen in Container」を選択

4. **コンテナのビルド**
   - 初回起動時は自動的にコンテナがビルドされます
   - Docker Composeで定義されたサービスが起動します

5. **開発開始**
    - コンテナ内でターミナルを開き、必要なコマンドを実行できます
    - 例えば、Frontendでは`bun dev`、Backendでは`uvicorn src.main:app --host 0.0.0.0 --reload`など

#### Dev Container の特徴

**共通機能：**
- Zsh + Oh My Zsh + Starshipによるリッチなターミナル環境

**Frontend Container：**
- Bun ランタイム
- Biome（フォーマッター/リンター）拡張機能

**Backend Container：**
- Python 3.13
- Ruff（Python リンター）拡張機能
- Python 拡張機能

#### プロジェクト構成

```
bychance-job/
├── frontend/               # Next.js アプリケーション
│   ├── .devcontainer/     # Frontend用Dev Container設定
│   ├── docker/           # Dockerfile
│   └── app/              # ソースコード
├── backend/               # FastAPI アプリケーション
│   ├── .devcontainer/     # Backend用Dev Container設定
│   ├── docker/           # Dockerfile
│   └── src/              # ソースコード
└── compose.yaml          # Docker Compose設定
```

#### 注意事項

- 各サービスは独立したDev Containerとして動作します
- ホストマシンのファイルは自動的にコンテナ内にマウントされます
- 変更は即座に反映されます（ホットリロード対応）
