#!/usr/bin/env python3
"""
設定駆動型書類生成スクリプト
shop-settings.yaml.sampleをsettings.yamlにコピーして使用します
申込者データを含めた書類生成も可能です
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


class DocumentGenerator:
    """書類生成クラス"""
    
    def __init__(self, settings_path='settings.yaml', applicant_path=None):
        """
        初期化
        
        Args:
            settings_path: 設定ファイルのパス
            applicant_path: 申込者データファイルのパス（オプション）
        """
        self.base_dir = Path(__file__).parent
        self.settings_path = self.base_dir / settings_path
        
        # settings.yamlが存在しない場合、shop-settings.yaml.sampleから作成を促す
        if not self.settings_path.exists():
            sample_path = self.base_dir / 'shop-settings.yaml.sample'
            if sample_path.exists():
                print(f"エラー: 設定ファイル '{settings_path}' が見つかりません。")
                print(f"以下のコマンドでサンプルから設定ファイルを作成してください：")
                print(f"  cp shop-settings.yaml.sample settings.yaml")
                sys.exit(1)
        
        self.settings = self._load_settings()
        
        # 申込者データの読み込み（指定された場合）
        self.applicant_data = None
        if applicant_path:
            self.applicant_path = self.base_dir / applicant_path
            self.applicant_data = self._load_applicant_data()
        
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
        self.env.filters['format_checkbox'] = self._format_checkbox
        
    def _load_settings(self):
        """設定ファイルを読み込む"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"エラー: 設定ファイル '{self.settings_path}' が見つかりません。")
            print(f"以下のコマンドでサンプルから設定ファイルを作成してください：")
            print(f"  cp shop-settings.yaml.sample settings.yaml")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"エラー: 設定ファイルの読み込みに失敗しました: {e}")
            sys.exit(1)
    
    def _load_applicant_data(self):
        """申込者データファイルを読み込む"""
        try:
            with open(self.applicant_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                print(f"✅ 申込者データを読み込みました: {self.applicant_path}")
                return data
        except FileNotFoundError:
            print(f"警告: 申込者データファイル '{self.applicant_path}' が見つかりません。")
            print("    空の申込書テンプレートを生成します。")
            return None
        except yaml.YAMLError as e:
            print(f"エラー: 申込者データファイルの読み込みに失敗しました: {e}")
            return None
            
    def _format_price(self, value):
        """価格をフォーマット"""
        return f"¥{value:,}"
        
    def _format_date(self, value):
        """日付をフォーマット"""
        if isinstance(value, str):
            return value
        return value.strftime('%Y年%m月%d日')
    
    def _format_checkbox(self, checked):
        """チェックボックスをフォーマット"""
        return '☑' if checked else '□'
        
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
            
            # 申込者データが存在する場合は追加
            if self.applicant_data:
                context['applicant'] = self.applicant_data.get('applicant', {})
                context['has_applicant_data'] = True
            else:
                context['has_applicant_data'] = False
            
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


def parse_arguments():
    """コマンドライン引数のパース"""
    parser = argparse.ArgumentParser(
        description='設定駆動型書類生成スクリプト',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 空の申込書テンプレートを生成
  python generator.py
  
  # 申込者データを含めた申込書を生成
  python generator.py --applicant applicant_data.yaml
  
  # 複数の申込者データを一括処理
  python generator.py --applicant-dir applicants/
        """
    )
    
    parser.add_argument(
        '--applicant',
        help='申込者データファイルのパス',
        type=str,
        default=None
    )
    
    parser.add_argument(
        '--applicant-dir',
        help='申込者データファイルのディレクトリ（一括処理）',
        type=str,
        default=None
    )
    
    parser.add_argument(
        '--settings',
        help='設定ファイルのパス（デフォルト: settings.yaml）',
        type=str,
        default='settings.yaml'
    )
    
    parser.add_argument(
        '--check',
        help='テンプレートファイルの存在確認のみ実行',
        action='store_true'
    )
    
    return parser.parse_args()


def process_single_applicant(settings_path, applicant_path=None):
    """単一の申込者データを処理"""
    generator = DocumentGenerator(
        settings_path=settings_path,
        applicant_path=applicant_path
    )
    
    # テンプレートの確認
    if not generator.validate_templates():
        print()
        print("テンプレートファイルを作成してから実行してください。")
        return False
        
    print()
    
    # 書類の生成
    generator.generate_all()
    return True


def process_batch_applicants(settings_path, applicant_dir):
    """複数の申込者データを一括処理"""
    applicant_dir = Path(applicant_dir)
    
    if not applicant_dir.exists():
        print(f"エラー: ディレクトリ '{applicant_dir}' が存在しません。")
        return False
        
    # YAMLファイルの検索
    yaml_files = list(applicant_dir.glob('*.yaml')) + list(applicant_dir.glob('*.yml'))
    
    if not yaml_files:
        print(f"警告: ディレクトリ '{applicant_dir}' にYAMLファイルが見つかりません。")
        return False
        
    print(f"📂 {len(yaml_files)}件の申込者データを処理します")
    print()
    
    success_count = 0
    for yaml_file in yaml_files:
        print(f"--- 処理中: {yaml_file.name} ---")
        if process_single_applicant(settings_path, str(yaml_file.relative_to(Path.cwd()))):
            success_count += 1
        print()
        
    print(f"📊 処理結果: {success_count}/{len(yaml_files)} 件成功")
    return success_count == len(yaml_files)


def main():
    """メイン処理"""
    args = parse_arguments()
    
    # チェックモード
    if args.check:
        generator = DocumentGenerator(settings_path=args.settings)
        if generator.validate_templates():
            print("\n✅ すべてのテンプレートファイルが存在します。")
            sys.exit(0)
        else:
            sys.exit(1)
    
    # 一括処理モード
    if args.applicant_dir:
        success = process_batch_applicants(args.settings, args.applicant_dir)
        sys.exit(0 if success else 1)
    
    # 単一処理モード
    success = process_single_applicant(args.settings, args.applicant)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()