#!/usr/bin/env python3
"""
PDFファイルを使った検索テスト（OpenSearchなし）
"""

import os
import PyPDF2
from start_opensearch import SimpleSearchEngine


def extract_text_from_pdf(pdf_path: str):
    """PDFからテキストを抽出"""
    pages_content = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    pages_content.append({
                        'filename': os.path.basename(pdf_path),
                        'file_path': pdf_path,
                        'content': text,
                        'page_number': page_num
                    })
                    
    except Exception as e:
        print(f"❌ PDFファイル読み込みエラー ({pdf_path}): {e}")
        
    return pages_content


def test_pdf_search():
    """PDFファイルの検索テスト"""
    
    # シンプル検索エンジンを初期化
    search_engine = SimpleSearchEngine()
    
    # PDFファイルのパス
    pdf_path = "./sample_pdfs/AIの変遷とエンジニアのキャリア.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDFファイルが見つかりません: {pdf_path}")
        print("sample_pdfsディレクトリにPDFファイルを配置してください")
        return
    
    print(f"📖 PDFファイルを読み込み中: {pdf_path}")
    
    # PDFからテキスト抽出
    pages_content = extract_text_from_pdf(pdf_path)
    
    if not pages_content:
        print("❌ PDFからテキストを抽出できませんでした")
        return
    
    print(f"✅ {len(pages_content)} ページを抽出しました")
    
    # 各ページをインデックス化
    for page_data in pages_content:
        doc_id = f"{page_data['filename']}_page_{page_data['page_number']}"
        search_engine.index_document(doc_id, page_data)
    
    # 検索テスト
    search_queries = ["AI", "エンジニア", "キャリア", "変遷", "テスト"]
    
    for query in search_queries:
        print(f"\n🔍 検索: '{query}'")
        results = search_engine.search(query, size=3)
        
        if results:
            print(f"   見つかった結果: {len(results)} 件")
            for i, result in enumerate(results[:2], 1):
                print(f"   [{i}] ページ {result['page_number']} - スコア: {result['score']}")
                # ハイライト表示（最初の100文字のみ）
                highlight = result['highlights'][0][:100] + "..." if len(result['highlights'][0]) > 100 else result['highlights'][0]
                print(f"       マッチ: {highlight}")
        else:
            print("   結果なし")
    
    # 統計表示
    print(f"\n📊 統計情報:")
    print(f"   総ページ数: {search_engine.count_documents()}")
    print(f"   ファイル数: {search_engine.get_unique_files()}")


if __name__ == "__main__":
    print("=== PDF検索テスト（OpenSearchなし） ===")
    test_pdf_search()
    print("\n✅ テスト完了！") 