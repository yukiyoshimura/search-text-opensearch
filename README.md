# PDF検索システム with OpenSearch
OpenSearchを使ってPDFファイルの中身に対してテキスト検索を行うシステムです。

## 機能

- PDFファイルからテキストを抽出してOpenSearchにインデックス化
- 高速なテキスト検索（部分一致、フレーズ検索）
- ページ単位での検索結果表示
- ハイライト機能付きの検索結果
- REST API対応
- コマンドライン インターフェース

## セットアップ

### Dev Container を使用した開発環境

1. Visual Studio Code で Dev Container 拡張機能をインストール
2. このプロジェクトを開く
3. コマンドパレット（Cmd+Shift+P）で「Dev Containers: Reopen in Container」を選択
4. コンテナのビルドが完了するまで待機

### 含まれるサービス

- **Python 3.11**: メインのアプリケーション環境
- **OpenSearch**: 全文検索エンジン（ポート 9200）
- **OpenSearch Dashboards**: 管理インターフェース（ポート 5601）

## 使用方法

### 1. 接続テスト

```bash
python test_connection.py
```

### 2. PDFファイルのインデックス化

```bash
# 単一ファイルのインデックス化
python src/search_cli.py index path/to/your/file.pdf

# ディレクトリ全体のインデックス化
python src/search_cli.py index ./sample_pdfs
```

### 3. テキスト検索

```bash
# コマンドラインでの検索
python src/search_cli.py search "テスト"

# 結果件数を指定
python src/search_cli.py search "サンプル" --size 5
```

### 4. 統計情報の確認

```bash
python src/search_cli.py stats
```

### 5. Web API の使用

```bash
# APIサーバーの起動
python src/search_api.py
```

#### API エンドポイント

- `GET /health` - ヘルスチェック
- `GET /search?q=検索文字&size=10` - テキスト検索
- `POST /search` - テキスト検索（JSONリクエスト）
- `GET /stats` - インデックス統計情報

### 6. 使用例の実行

```bash
python example_usage.py
```

## 検索例

PDFファイルに「テスト」という文字が含まれている場合：

```bash
python src/search_cli.py search "テスト"
```

結果例：
```
🔍 検索結果: 'テスト' (件数: 2)
============================================================

【1】sample.pdf (ページ 1)
スコア: 2.15
マッチ箇所:
  • この文書は<em>テスト</em>用のサンプルです
  • <em>テスト</em>を実行して確認してください

【2】manual.pdf (ページ 5)
スコア: 1.89
内容プレビュー:
システムの動作テストについて説明します...
```
