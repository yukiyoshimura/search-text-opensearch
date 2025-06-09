#!/usr/bin/env python3
"""
OpenSearchとの接続をテストするスクリプト
"""

import time
import requests
from opensearchpy import OpenSearch

def test_opensearch_connection():
    """OpenSearchとの接続をテストする"""
    
    # OpenSearchクライアントの設定
    client = OpenSearch(
        hosts=[{'host': 'opensearch-node1', 'port': 9200}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    
    # 接続テスト
    try:
        print("OpenSearchへの接続をテスト中...")
        
        # クラスター情報の取得
        info = client.info()
        print(f"✅ OpenSearch接続成功!")
        print(f"   バージョン: {info['version']['number']}")
        print(f"   クラスター名: {info['cluster_name']}")
        
        # インデックス一覧の取得
        indices = client.indices.get_alias(index="*")
        print(f"   既存インデックス数: {len(indices)}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenSearch接続エラー: {e}")
        return False

def test_http_connection():
    """HTTP経由でのOpenSearch接続をテストする"""
    try:
        print("HTTP経由での接続をテスト中...")
        response = requests.get('http://opensearch-node1:9200')
        if response.status_code == 200:
            print("✅ HTTP接続成功!")
            return True
        else:
            print(f"❌ HTTP接続失敗: ステータスコード {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HTTP接続エラー: {e}")
        return False

if __name__ == "__main__":
    print("=== OpenSearch接続テスト ===")
    
    # HTTP接続テスト
    if test_http_connection():
        time.sleep(2)
        # OpenSearchクライアント接続テスト
        test_opensearch_connection()
    
    print("\n=== テスト完了 ===") 