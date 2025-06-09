#!/usr/bin/env python3
"""
OpenSearchの代替として、メモリ内検索システムを提供
（開発・テスト用）
"""

import json
import re
from typing import List, Dict, Any


class SimpleSearchEngine:
    """シンプルなメモリ内検索エンジン（OpenSearchの代替）"""
    
    def __init__(self):
        self.documents = {}
        self.index_name = 'pdf_documents'
    
    def index_document(self, doc_id: str, document: Dict[str, Any]):
        """ドキュメントをインデックス化"""
        self.documents[doc_id] = document
        print(f"✅ ドキュメント '{doc_id}' をインデックス化しました")
    
    def search(self, query: str, size: int = 10) -> List[Dict[str, Any]]:
        """テキスト検索を実行"""
        results = []
        
        for doc_id, doc in self.documents.items():
            content = doc.get('content', '').lower()
            query_lower = query.lower()
            
            # 簡単な検索（部分一致）
            if query_lower in content:
                # スコア計算（マッチ回数）
                score = content.count(query_lower)
                
                # ハイライト生成
                highlighted_content = re.sub(
                    f'({re.escape(query)})',
                    r'<em>\1</em>',
                    doc.get('content', ''),
                    flags=re.IGNORECASE
                )
                
                # コンテンツプレビュー
                preview = doc.get('content', '')[:300]
                if len(doc.get('content', '')) > 300:
                    preview += "..."
                
                result = {
                    'filename': doc.get('filename', 'unknown'),
                    'file_path': doc.get('file_path', 'unknown'),
                    'page_number': doc.get('page_number', 1),
                    'score': float(score),
                    'content_preview': preview,
                    'highlights': [highlighted_content[:200] + "..."] if len(highlighted_content) > 200 else [highlighted_content]
                }
                
                results.append(result)
        
        # スコア順でソート
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:size]
    
    def count_documents(self) -> int:
        """ドキュメント数を返す"""
        return len(self.documents)
    
    def get_unique_files(self) -> int:
        """ユニークなファイル数を返す"""
        filenames = set()
        for doc in self.documents.values():
            filenames.add(doc.get('filename', 'unknown'))
        return len(filenames)


def test_simple_search():
    """シンプル検索エンジンのテスト"""
    engine = SimpleSearchEngine()
    
    # テストドキュメントを追加
    engine.index_document('test1_page_1', {
        'filename': 'test1.pdf',
        'file_path': '/test/test1.pdf',
        'content': 'これはテスト用のドキュメントです。AIについて説明します。',
        'page_number': 1
    })
    
    engine.index_document('test2_page_1', {
        'filename': 'test2.pdf', 
        'file_path': '/test/test2.pdf',
        'content': 'サンプルテキストファイルです。テストを実行してください。',
        'page_number': 1
    })
    
    # 検索テスト
    print("\n🔍 検索テスト: 'テスト'")
    results = engine.search('テスト')
    
    for i, result in enumerate(results, 1):
        print(f"\n【{i}】{result['filename']} (ページ {result['page_number']})")
        print(f"スコア: {result['score']}")
        print(f"ハイライト: {result['highlights'][0]}")
    
    print(f"\n📊 統計:")
    print(f"総ドキュメント数: {engine.count_documents()}")
    print(f"ユニークファイル数: {engine.get_unique_files()}")


if __name__ == "__main__":
    print("=== シンプル検索エンジンのテスト ===")
    test_simple_search()
    
    print("\n💡 OpenSearchが利用できない場合は、このシンプル検索エンジンを")
    print("   PDFSearchManagerの代替として使用できます。") 