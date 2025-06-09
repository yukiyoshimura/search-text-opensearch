#!/usr/bin/env python3
"""
PDFファイル検索のコマンドラインツール
"""

import argparse
import sys
from pdf_search import PDFSearchManager


def main():
    parser = argparse.ArgumentParser(
        description='OpenSearchを使用してPDFファイルを検索'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # インデックス化コマンド
    index_parser = subparsers.add_parser(
        'index', 
        help='PDFファイルまたはディレクトリをインデックス化'
    )
    index_parser.add_argument(
        'path', 
        help='PDFファイルまたはディレクトリのパス'
    )
    
    # 検索コマンド
    search_parser = subparsers.add_parser(
        'search', 
        help='テキスト検索を実行'
    )
    search_parser.add_argument(
        'query', 
        help='検索したいテキスト'
    )
    search_parser.add_argument(
        '--size', 
        type=int, 
        default=10, 
        help='結果の最大件数 (デフォルト: 10)'
    )
    
    # 統計コマンド
    stats_parser = subparsers.add_parser(
        'stats', 
        help='インデックスの統計情報を表示'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # PDFSearchManagerを初期化
    try:
        search_manager = PDFSearchManager()
    except Exception as e:
        print(f"❌ OpenSearchへの接続エラー: {e}")
        sys.exit(1)
    
    # コマンドに応じて処理を実行
    if args.command == 'index':
        import os
        if os.path.isfile(args.path):
            # 単一ファイルのインデックス化
            if search_manager.index_pdf(args.path):
                print("✅ インデックス化が完了しました")
            else:
                print("❌ インデックス化に失敗しました")
                sys.exit(1)
        elif os.path.isdir(args.path):
            # ディレクトリ全体のインデックス化
            results = search_manager.index_pdf_directory(args.path)
            if results['failed']:
                sys.exit(1)
        else:
            print(f"❌ パスが見つかりません: {args.path}")
            sys.exit(1)
    
    elif args.command == 'search':
        results = search_manager.search_text(args.query, size=args.size)
        
        if not results:
            print("検索結果がありませんでした")
            return
        
        print(f"\n🔍 検索結果: '{args.query}' (件数: {len(results)})")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"\n【{i}】{result['filename']} (ページ {result['page_number']})")
            print(f"スコア: {result['score']:.2f}")
            
            # ハイライト表示
            if 'highlights' in result:
                print("マッチ箇所:")
                for highlight in result['highlights']:
                    print(f"  • {highlight}")
            else:
                print(f"内容プレビュー:\n{result['content_preview']}")
            
            print("-" * 40)
    
    elif args.command == 'stats':
        stats = search_manager.get_document_stats()
        if stats:
            print("\n📊 インデックス統計情報")
            print("=" * 30)
            print(f"インデックス名: {stats['index_name']}")
            print(f"登録ファイル数: {stats['unique_files']}")
            print(f"総ページ数: {stats['total_pages']}")
        else:
            print("統計情報を取得できませんでした")


if __name__ == "__main__":
    main() 