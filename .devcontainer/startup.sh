#!/bin/bash

echo "OpenSearchの起動を待機中..."

# OpenSearchが起動するまで待機
while ! curl -s http://opensearch-node1:9200 > /dev/null; do
    echo "OpenSearchの起動を待機中..."
    sleep 5
done

echo "OpenSearchが起動しました！"
echo "OpenSearch: http://localhost:9200"
echo "OpenSearch Dashboards: http://localhost:5601"

# 基本的なインデックスを作成
curl -X PUT "opensearch-node1:9200/documents" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "filename": { "type": "text" },
      "content": { "type": "text" },
      "file_type": { "type": "keyword" },
      "upload_date": { "type": "date" }
    }
  }
}'

echo -e "\n文書インデックスが作成されました！" 