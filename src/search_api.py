#!/usr/bin/env python3
"""
PDFファイル検索のFlask API
"""

from flask import Flask, request, jsonify
from pdf_search import PDFSearchManager

app = Flask(__name__)

# PDFSearchManagerのグローバルインスタンス
search_manager = None


def init_search_manager():
    """検索マネージャーを初期化"""
    global search_manager
    try:
        search_manager = PDFSearchManager()
        return True
    except Exception as e:
        print(f"OpenSearch接続エラー: {e}")
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """ヘルスチェック"""
    return jsonify({
        'status': 'ok',
        'service': 'PDF Search API'
    })


@app.route('/search', methods=['GET'])
def search_text():
    """テキスト検索API"""
    if not search_manager:
        return jsonify({'error': 'Search manager not initialized'}), 500
    
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'クエリパラメータ "q" が必要です'}), 400
    
    try:
        size = int(request.args.get('size', 10))
        if size < 1 or size > 100:
            size = 10
    except ValueError:
        size = 10
    
    try:
        results = search_manager.search_text(query, size=size)
        
        return jsonify({
            'query': query,
            'total_results': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'検索エラー: {str(e)}'}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """統計情報API"""
    if not search_manager:
        return jsonify({'error': 'Search manager not initialized'}), 500
    
    try:
        stats = search_manager.get_document_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': f'統計取得エラー: {str(e)}'}), 500


@app.route('/search', methods=['POST'])
def search_text_post():
    """テキスト検索API (POST)"""
    if not search_manager:
        return jsonify({'error': 'Search manager not initialized'}), 500
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'JSON body with "query" field required'}), 400
    
    query = data['query'].strip()
    if not query:
        return jsonify({'error': 'クエリが空です'}), 400
    
    size = data.get('size', 10)
    try:
        size = int(size)
        if size < 1 or size > 100:
            size = 10
    except ValueError:
        size = 10
    
    try:
        results = search_manager.search_text(query, size=size)
        
        return jsonify({
            'query': query,
            'total_results': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'検索エラー: {str(e)}'}), 500


if __name__ == '__main__':
    if init_search_manager():
        print("🚀 PDF検索APIをポート8000で開始します...")
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        print("❌ 検索マネージャーの初期化に失敗しました")
        exit(1) 