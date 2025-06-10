#!/usr/bin/env python3
"""
PDFファイルをOpenSearchにインデックス化し、検索する機能
"""

import os
import PyPDF2
from typing import List, Dict, Any
from opensearchpy import OpenSearch


class PDFSearchManager:
    def __init__(self, opensearch_host='opensearch-node1',
                 opensearch_port=9200):
        """OpenSearchクライアントを初期化"""
        self.client = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': opensearch_port}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
        self.index_name = 'pdf_documents'
        self._create_index_if_not_exists()
    
    def _create_index_if_not_exists(self):
        """インデックスが存在しない場合は作成する"""
        if not self.client.indices.exists(index=self.index_name):
            # インデックスマッピングの定義
            mapping = {
                "mappings": {
                    "properties": {
                        "filename": {
                            "type": "keyword"
                        },
                        "file_path": {
                            "type": "keyword"
                        },
                        "content": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "page_number": {
                            "type": "integer"
                        },
                        "indexed_at": {
                            "type": "date"
                        }
                    }
                }
            }
            
            # インデックス作成
            self.client.indices.create(
                index=self.index_name,
                body=mapping
            )
            print(f"✅ インデックス '{self.index_name}' を作成しました")
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """PDFファイルからテキストを抽出し、ページごとに分割する"""
        pages_content = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():  # 空でないページのみ
                        pages_content.append({
                            'filename': os.path.basename(pdf_path),
                            'file_path': pdf_path,
                            'content': text,
                            'page_number': page_num
                        })
                
        except Exception as e:
            print(f"❌ PDFファイル読み込みエラー ({pdf_path}): {e}")
            
        return pages_content
    
    def index_pdf(self, pdf_path: str) -> bool:
        """PDFファイルをOpenSearchにインデックス化する"""
        if not os.path.exists(pdf_path):
            print(f"❌ ファイルが見つかりません: {pdf_path}")
            return False
        
        # PDFからテキスト抽出
        pages_content = self.extract_text_from_pdf(pdf_path)
        
        if not pages_content:
            print(f"❌ PDFからテキストを抽出できませんでした: {pdf_path}")
            return False
        
        # 各ページをインデックス化
        for page_data in pages_content:
            doc_id = f"{page_data['filename']}_page_{page_data['page_number']}"
            
            try:
                self.client.index(
                    index=self.index_name,
                    id=doc_id,
                    body={
                        **page_data,
                        'indexed_at': '2024-01-01T00:00:00Z'
                    }
                )
                
            except Exception as e:
                print(f"❌ インデックス化エラー "
                      f"(ページ {page_data['page_number']}): {e}")
                return False
        
        filename = os.path.basename(pdf_path)
        page_count = len(pages_content)
        print(f"✅ PDF '{filename}' を {page_count} ページインデックス化しました")
        return True
    
    def index_pdf_directory(self, directory_path: str) -> Dict[str, Any]:
        """ディレクトリ内の全PDFファイルをインデックス化する"""
        results = {
            'success': [],
            'failed': [],
            'total_files': 0
        }
        
        if not os.path.exists(directory_path):
            print(f"❌ ディレクトリが見つかりません: {directory_path}")
            return results
        
        # PDFファイルを検索
        pdf_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        results['total_files'] = len(pdf_files)
        
        # 各PDFファイルをインデックス化
        for pdf_path in pdf_files:
            if self.index_pdf(pdf_path):
                results['success'].append(pdf_path)
            else:
                results['failed'].append(pdf_path)
        
        print("\n📊 インデックス化結果:")
        print(f"   成功: {len(results['success'])} ファイル")
        print(f"   失敗: {len(results['failed'])} ファイル")
        print(f"   合計: {results['total_files']} ファイル")
        
        return results
    
    def search_text(self, query: str, size: int = 10) -> List[Dict[str, Any]]:
        """テキスト検索を実行する"""
        search_body = {
            "query": {
                "match": {
                    "content": {
                        "query": query,
                        "operator": "and"
                    }
                }
            },
            "highlight": {
                "fields": {
                    "content": {
                        "fragment_size": 200,
                        "number_of_fragments": 3
                    }
                }
            },
            "size": size,
            "_source": ["filename", "file_path", "page_number", "content"]
        }
        
        try:
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            results = []
            for hit in response['hits']['hits']:
                content = hit['_source']['content']
                content_preview = (content[:300] + "..."
                                   if len(content) > 300 else content)
                
                result = {
                    'filename': hit['_source']['filename'],
                    'file_path': hit['_source']['file_path'],
                    'page_number': hit['_source']['page_number'],
                    'score': hit['_score'],
                    'content_preview': content_preview
                }
                
                # ハイライト情報があれば追加
                if 'highlight' in hit:
                    result['highlights'] = hit['highlight'].get('content', [])
                
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ 検索エラー: {e}")
            return []
    
    def get_document_stats(self) -> Dict[str, Any]:
        """インデックス内のドキュメント統計を取得する"""
        try:
            # ドキュメント数
            count_response = self.client.count(index=self.index_name)
            total_docs = count_response['count']
            
            # ファイル数（ユニークなファイル名）
            unique_files_query = {
                "aggs": {
                    "unique_files": {
                        "cardinality": {
                            "field": "filename"
                        }
                    }
                },
                "size": 0
            }
            
            agg_response = self.client.search(
                index=self.index_name,
                body=unique_files_query
            )
            
            unique_files = (agg_response['aggregations']
                            ['unique_files']['value'])
            
            return {
                'total_pages': total_docs,
                'unique_files': unique_files,
                'index_name': self.index_name
            }
            
        except Exception as e:
            print(f"❌ 統計取得エラー: {e}")
            return {} 