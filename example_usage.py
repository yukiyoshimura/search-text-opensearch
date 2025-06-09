#!/usr/bin/env python3
"""
PDF検索システムの使用例
"""

import os
from src.pdf_search import PDFSearchManager


def example_usage():
    """使用例のデモンストレーション"""
    
    print("🔍 PDF検索システムの使用例")
    print("=" * 50)
    
    # 1. PDFSearchManagerの初期化
    try:
        search_manager = PDFSearchManager()
        print("✅ OpenSearch接続成功")
    except Exception as e:
        print(f"❌ OpenSearch接続エラー: {e}")
        return
    
    # 2. サンプルPDFファイルがある場合のインデックス化
    sample_pdf_dir = "./sample_pdfs"
    if os.path.exists(sample_pdf_dir):
        print(f"\n📁 ディレクトリ '{sample_pdf_dir}' のPDFファイルをインデックス化中...")
        results = search_manager.index_pdf_directory(sample_pdf_dir)
        
        if results['success']:
            print("✅ インデックス化完了!")
        else:
            print("⚠️  インデックス化するPDFファイルがありませんでした")
    else:
        print(f"\n⚠️  サンプルディレクトリ '{sample_pdf_dir}' が見つかりません")
        print("PDFファイルを配置してからお試しください")
    
    # 3. 統計情報の表示
    print("\n📊 現在のインデックス統計:")
    stats = search_manager.get_document_stats()
    if stats:
        print(f"   登録ファイル数: {stats.get('unique_files', 0)}")
        print(f"   総ページ数: {stats.get('total_pages', 0)}")
    else:
        print("   統計情報を取得できませんでした")
    
    # 4. 検索例
    search_queries = ["テスト", "サンプル", "example", "test"]
    
    for query in search_queries:
        print(f"\n🔍 検索: '{query}'")
        results = search_manager.search_text(query, size=3)
        
        if results:
            print(f"   見つかった結果: {len(results)} 件")
            for i, result in enumerate(results[:2], 1):  # 最初の2件のみ表示
                print(f"   [{i}] {result['filename']} - ページ {result['page_number']}")
                print(f"       スコア: {result['score']:.2f}")
        else:
            print("   結果なし")
    
    print("\n✅ 使用例のデモ完了")


def create_sample_directory():
    """サンプルディレクトリを作成"""
    sample_dir = "./sample_pdfs"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
        print(f"📁 サンプルディレクトリ '{sample_dir}' を作成しました")
        print("このディレクトリにPDFファイルを配置してください")
    else:
        print(f"📁 サンプルディレクトリ '{sample_dir}' は既に存在します")


if __name__ == "__main__":
    print("PDF検索システムのセットアップと使用例")
    print("=" * 60)
    
    # サンプルディレクトリの作成
    create_sample_directory()
    
    print("\n" + "=" * 60)
    
    # 使用例の実行
    example_usage()
    
    print("\n" + "=" * 60)
    print("📝 コマンドラインでの使用方法:")
    print("   python src/search_cli.py index ./sample_pdfs")
    print("   python src/search_cli.py search 'テスト'")
    print("   python src/search_cli.py stats")
    print("\n🌐 APIサーバーの起動:")
    print("   python src/search_api.py") 