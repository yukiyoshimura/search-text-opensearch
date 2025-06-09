#!/usr/bin/env python3
"""
シンプルなOpenSearchヘルスチェック
"""

import sys
import time
import requests

def check_opensearch():
    """OpenSearchの起動を確認"""
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get('http://opensearch-node1:9200', timeout=5)
            if response.status_code == 200:
                print("✅ OpenSearchが起動しました!")
                print("🌐 http://localhost:9200")
                print("📊 Dashboard: http://localhost:5601")
                return True
        except Exception as e:
            pass
        
        attempt += 1
        print(f"⏳ OpenSearchの起動を待機中... ({attempt}/{max_attempts})")
        time.sleep(2)
    
    print("❌ OpenSearchの起動に失敗しました")
    return False

if __name__ == "__main__":
    if check_opensearch():
        sys.exit(0)
    else:
        sys.exit(1) 