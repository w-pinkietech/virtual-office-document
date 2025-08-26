#!/usr/bin/env python3
"""
設定駆動型書類生成スクリプト
settings.yamlから契約書類を自動生成します
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


class DocumentGenerator:
    """書類生成クラス"""
    
    def __init__(self, settings_path='settings.yaml'):
        """
        初期化
        
        Args:
            settings_path: 設定ファイルのパス
        """
        self.base_dir = Path(__file__).parent
        self.settings_path = self.base_dir / settings_path
        self.settings = self._load_settings()
        
        # Jinja2環境の設定
        self.env = Environment(
            loader=FileSystemLoader(self.base_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # カスタムフィルターの追加
        self.env.filters['format_price'] = self._format_price
        self.env.filters['format_date'] = self._format_date
        
    def _load_settings(self):
        """設定ファイルを読み込む"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"エラー: 設定ファイル '{self.settings_path}' が見つかりません。")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"エラー: 設定ファイルの読み込みに失敗しました: {e}")
            sys.exit(1)
            
    def _format_price(self, value):
        """価格をフォーマット"""
        return f"¥{value:,}"
        
    def _format_date(self, value):
        """日付をフォーマット"""
        if isinstance(value, str):
            return value
        return value.strftime('%Y年%m月%d日')
        
    def generate_document(self, document_config):
        """
        単一の書類を生成
        
        Args:
            document_config: 書類設定辞書
        """
        template_path = document_config['template']
        # outputsフォルダに出力するよう変更
        output_filename = Path(document_config['output']).name
        output_path = self.base_dir / 'outputs' / output_filename
        
        try:
            # テンプレートの読み込み
            template = self.env.get_template(template_path)
            
            # テンプレート変数の準備
            context = {
                'org': self.settings['organization'],
                'legal': self.settings['legal'],
                'services': self.settings['services'],
                'terms': self.settings['terms'],
                'payment_methods': self.settings['payment_methods'],
                'mail_rules': self.settings['mail_rules'],
                'eligibility': self.settings['eligibility'],
                'prohibited_actions': self.settings['prohibited_actions'],
                'document_info': self.settings['document_info'],
                'today': datetime.now(),
            }
            
            # 書類の生成
            content = template.render(**context)
            
            # 出力ディレクトリの作成
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ファイルの書き込み
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✅ 生成完了: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ エラー: {document_config['title']} の生成に失敗: {e}")
            return False
            
    def generate_all(self):
        """全ての書類を生成"""
        print("📝 書類生成を開始します...")
        print(f"   設定ファイル: {self.settings_path}")
        print()
        
        documents = self.settings.get('documents', [])
        if not documents:
            print("警告: 生成する書類が設定されていません。")
            return
            
        success_count = 0
        for doc in documents:
            if self.generate_document(doc):
                success_count += 1
                
        print()
        print(f"📊 結果: {success_count}/{len(documents)} 件の書類を生成しました。")
        
        if success_count == len(documents):
            print("✨ すべての書類が正常に生成されました。")
        else:
            print("⚠️  一部の書類の生成に失敗しました。")
            sys.exit(1)
            
    def validate_templates(self):
        """テンプレートファイルの存在確認"""
        print("🔍 テンプレートファイルを確認中...")
        
        documents = self.settings.get('documents', [])
        missing_templates = []
        
        for doc in documents:
            template_path = self.base_dir / doc['template']
            if not template_path.exists():
                missing_templates.append(doc['template'])
                print(f"   ❌ {doc['template']} - 存在しません")
            else:
                print(f"   ✅ {doc['template']} - OK")
                
        if missing_templates:
            print()
            print("エラー: 以下のテンプレートファイルが見つかりません:")
            for path in missing_templates:
                print(f"  - {path}")
            return False
            
        print("   すべてのテンプレートが存在します。")
        return True


def main():
    """メイン処理"""
    generator = DocumentGenerator()
    
    # テンプレートの確認
    if not generator.validate_templates():
        print()
        print("テンプレートファイルを作成してから実行してください。")
        sys.exit(1)
        
    print()
    
    # 書類の生成
    generator.generate_all()


if __name__ == '__main__':
    main()