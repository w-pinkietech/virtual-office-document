# 設定駆動型書類生成システム

バーチャルオフィス契約書類をsettings.yamlから自動生成するシステムです。

## 📁 ディレクトリ構造

```
10_legal-documents/
├── settings.yaml.sample   # 設定ファイルのサンプル
├── settings.yaml          # 実際の設定ファイル（.gitignore対象）
├── applicant_data.yaml.sample  # 申込者データのサンプル
├── applicant_data.yaml    # 申込者データ（.gitignore対象）
├── generator.py           # 書類生成スクリプト
├── requirements.txt       # Pythonパッケージ定義
├── .gitignore            # Git除外設定
├── templates/             # Jinja2テンプレート
│   ├── application_form.md.j2       # 申込書テンプレート
│   ├── terms_of_service.md.j2       # 会員規約テンプレート
│   └── postal_contract_corporate.md.j2  # 郵便サービス契約書テンプレート
├── current/              # サンプル書類（変更しない）
│   ├── バーチャルオフィス申込書.md
│   ├── 会員規約.md
│   └── 郵便サービス契約書_法人.md
├── outputs/              # 生成された書類（.gitignore対象）
│   ├── バーチャルオフィス申込書.md
│   ├── 会員規約.md
│   └── 郵便サービス契約書_法人.md
├── applicants/           # 複数申込者データ格納用（.gitignore対象）
│   └── *.yaml
└── README.md            # このファイル
```

## 🔧 環境準備

### Python仮想環境の作成とパッケージインストール

#### 方法1: venvを使用（推奨）

```bash
# 仮想環境の作成
cd 10_legal-documents
python3 -m venv venv

# 仮想環境の有効化
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# パッケージのインストール
pip install -r requirements.txt
```

#### 方法2: pipenvを使用

```bash
cd 10_legal-documents
pipenv install -r requirements.txt
pipenv shell
```

#### 方法3: グローバルインストール（非推奨）

```bash
cd 10_legal-documents
pip install -r requirements.txt
```

### 必要なPythonパッケージ

`requirements.txt`に定義されているパッケージ：
- **PyYAML** (6.0.1) - YAML設定ファイルの読み込み
- **Jinja2** (3.1.4) - テンプレートエンジン

### 仮想環境の無効化

作業終了後、仮想環境を無効化する場合：

```bash
# venvの場合
deactivate

# pipenvの場合
exit
```

## 🚀 使用方法

### 1. 初期設定

初回実行時は、サンプルから設定ファイルをコピーします：

```bash
cp settings.yaml.sample settings.yaml
```

### 2. 設定の変更

`settings.yaml`を編集して、組織情報や料金等を更新します：

```yaml
organization:
  name: マルスカフェ
  tel: "[電話番号]"  # TODO: 実際の番号を設定
  email: "[メールアドレス]"  # TODO: 実際のメールを設定
  
services:
  virtual_office:
    price: 2200  # 料金変更時はここを編集
```

### 3. 書類の生成

#### 基本的な使用方法（空の申込書テンプレート）

```bash
cd 10_legal-documents
python generator.py
```

実行結果例：
```
📝 書類生成を開始します...
✅ 生成完了: outputs/バーチャルオフィス申込書.md
✅ 生成完了: outputs/会員規約.md
✅ 生成完了: outputs/郵便サービス契約書_法人.md
✨ すべての書類が正常に生成されました。
```

#### 申込者データを含めた書類生成

申込者の情報を事前に入力した書類を生成する場合：

1. サンプルから申込者データファイルをコピー：
```bash
cp applicant_data.yaml.sample applicant_data.yaml
```

2. `applicant_data.yaml`を編集して申込者情報を入力

3. 申込者データを含めて書類を生成：
```bash
python generator.py --applicant applicant_data.yaml
```

#### 複数申込者の一括処理

```bash
# applicants/フォルダに複数の申込者データを配置
python generator.py --applicant-dir applicants/
```

#### その他のオプション

```bash
# テンプレートファイルの存在確認のみ
python generator.py --check

# 設定ファイルを指定
python generator.py --settings custom_settings.yaml

# ヘルプの表示
python generator.py --help
```

**注意**: 生成された書類は`outputs/`フォルダに保存されます。`current/`フォルダのファイルは変更されないサンプルです。

## 📋 設定項目

### 主要な設定項目

| カテゴリ | 項目 | 説明 |
|---------|------|------|
| organization | name, address, tel, email | 組織の基本情報 |
| services | virtual_office, mail_receipt, mail_forward | サービス料金設定 |
| terms | min_age, notice_period_months, mail_retention | 契約条件 |
| payment_methods | bank_transfer, direct_debit | 支払い方法 |
| mail_rules | prohibited_items, special_handling | 郵便物取扱いルール |
| legal | jurisdiction, applicable_law | 法務情報 |

## 🔧 カスタマイズ

### 新しい書類を追加する場合

1. `templates/`に新しいテンプレートを作成
2. `settings.yaml`の`documents`セクションに追加：

```yaml
documents:
  - id: new_document
    title: 新しい書類
    template: templates/new_document.md.j2
    output: current/新しい書類.md
```

3. `python generator.py`を実行

### テンプレート変数

テンプレート内で使用可能な主な変数：

- `{{ org }}` - 組織情報
- `{{ services }}` - サービス情報
- `{{ terms }}` - 契約条件
- `{{ payment_methods }}` - 支払い方法
- `{{ mail_rules }}` - 郵便物ルール
- `{{ document_info }}` - 書類メタデータ

## 🔍 動作確認

生成された書類は`outputs/`ディレクトリに保存されます。
以下で内容を確認できます：

```bash
# 申込書の確認
cat outputs/バーチャルオフィス申込書.md

# 会員規約の確認
cat outputs/会員規約.md

# 郵便サービス契約書の確認
cat outputs/郵便サービス契約書_法人.md
```

## 📝 注意事項

- `settings.yaml`は`.gitignore`に含まれるため、Gitには追跡されません
- `applicant_data.yaml`と`applicants/`フォルダも`.gitignore`対象のため、申込者の個人情報は保護されます
- `outputs/`フォルダも`.gitignore`対象のため、生成物はGitに含まれません
- `current/`フォルダのファイルはサンプルとして保持され、変更しないでください
- 電話番号、メールアドレス、ウェブサイトは実際の情報に置き換えてください
- 料金や条件を変更した場合は必ず再生成してください
- 申込者データファイルには個人情報が含まれるため、適切に管理してください

## 🛠️ トラブルシューティング

### エラー: テンプレートファイルが見つからない

```bash
# テンプレートの存在確認
ls -la templates/
```

### エラー: YAMLエラー

```bash
# settings.yamlの構文チェック
python -c "import yaml; yaml.safe_load(open('settings.yaml'))"
```


---

最終更新: 2025年8月27日