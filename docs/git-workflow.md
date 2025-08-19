# Git運用ワークフロー

> **GitHub運用ルール完全ガイド**  
> ブランチ戦略・Issue管理・プルリクエストの統合ワークフロー

## 🌳 ブランチ戦略

### ブランチ構成

```
main (プロダクション)
├── develop (開発ブランチ・デフォルト)
    ├── feature/legal-compliance-enhancement
    ├── feature/document-revision
    ├── ai/contract-legal-compliance-fix
    ├── hotfix/critical-legal-fix
    └── release/v2.0.0
```

### ブランチの役割

#### `main` - プロダクションブランチ
- **目的**: 専門家承認済みの安定版
- **保護**: 直接プッシュ禁止、PR必須
- **マージ条件**: 専門家レビュー完了 + 全チェック通過

#### `develop` - 開発ブランチ（デフォルト）
- **目的**: 開発作業の統合ブランチ
- **保護**: 直接プッシュ禁止、PR必須
- **マージ条件**: コードレビュー + CI通過

#### `feature/*` - 機能開発ブランチ
- **命名規則**: `feature/[epic-number]-[brief-description]`
- **例**: `feature/123-aml-compliance-enhancement`
- **開始点**: `develop`
- **マージ先**: `develop`

#### `ai/*` - AI提案ブランチ
- **命名規則**: `ai/[変更内容の概要]`
- **例**: `ai/contract-legal-compliance-fix`, `ai/privacy-policy-update`
- **開始点**: `develop`
- **マージ先**: `develop`（人間レビュー必須）
- **特徴**: AI生成の変更案、必須人間レビュー

#### `hotfix/*` - 緊急修正ブランチ
- **命名規則**: `hotfix/[issue-number]-[brief-description]`
- **例**: `hotfix/456-privacy-policy-urgent-fix`
- **開始点**: `main`
- **マージ先**: `main` および `develop`

#### `release/*` - リリース準備ブランチ
- **命名規則**: `release/v[version]`
- **例**: `release/v1.2.0`
- **開始点**: `develop`
- **マージ先**: `main` および `develop`

### ブランチ保護ルール

#### `main` ブランチ
- [ ] 直接プッシュを禁止
- [ ] PRマージ前に以下を必須とする：
  - [ ] 専門家レビュー（弁護士または行政書士）
  - [ ] プロジェクト管理者の承認
  - [ ] 全ステータスチェックの通過
  - [ ] 最新のdevelopブランチとの同期

#### `develop` ブランチ
- [ ] 直接プッシュを禁止
- [ ] PRマージ前に以下を必須とする：
  - [ ] 最低1名のコードレビュー
  - [ ] 全ステータスチェックの通過
  - [ ] 法務チェックリストの確認

---

## 📋 Issue管理

### Issue種別と使い分け

| 種別 | 用途 | ラベル | テンプレート | Todo対応 |
|------|------|--------|-------------|----------|
| **Epic** | 大きな機能・改善項目 | `epic` | epic-ai-template.md | TodoWriteの全体タスク |
| **Story** | Epicを構成する具体的作業 | `story` | story-ai-template.md | 個々のTodo項目 |
| **Bug** | 不具合・法的問題 | `bug` | bug.yml | 緊急Todo項目 |
| **Task** | その他の独立した作業 | `task` | task.yml | 単発Todo項目 |
| **AI Proposal** | AI提案・変更案 | `ai-proposal` | 全AIissueに自動付与 | 全AI作業に適用 |

### Epic-Story-Todo階層構造

```
Epic (GitHub Issue)
├── 📋 全体タスクの概要・目的
├── 🎯 完了条件・法的影響度
│
├── Story 1 (GitHub Issue) ↔ Todo ID: 1
│   ├── 📋 具体的作業内容
│   ├── ✅ 受け入れ条件
│   └── 🔄 進捗: pending → in_progress → completed
│
├── Story 2 (GitHub Issue) ↔ Todo ID: 2
│   ├── 📋 具体的作業内容
│   ├── ✅ 受け入れ条件
│   └── 🔄 進捗: pending → in_progress → completed
│
└── Story 3 (GitHub Issue) ↔ Todo ID: 3
    ├── 📋 具体的作業内容
    ├── ✅ 受け入れ条件
    ├── 💬 Task Comments (Sub-todo)
    │   ├── Sub-task 3.1
    │   └── Sub-task 3.2
    └── 🔄 進捗: pending → in_progress → completed
```

### Todo-Issue同期マッピング

| TodoWrite Level | GitHub Issue Type | 関係性 | 管理方法 |
|-----------------|-------------------|--------|----------|
| **全体タスク群** | Epic | 1対1 | TodoWrite実行時に自動Epic作成 |
| **個別Todo** | Story | 1対1 | Todo毎にStory作成・状態同期 |
| **Sub-todo** | Story Comment | 1対多 | Story内のタスクコメント |

### AI作業時のIssue階層例

```bash
# 例: AI作業「契約書の法的コンプライアンス改善」
TodoWrite -> 
  Todo 1: 個人情報保護方針の更新
  Todo 2: 利用規約の消費者契約法適合
  Todo 3: 郵便物転送規約の信書規制対応

GitHub Issues:
Epic #123: 契約書の法的コンプライアンス改善
├── Story #124: 個人情報保護方針の更新 (Todo ID: 1)
├── Story #125: 利用規約の消費者契約法適合 (Todo ID: 2)  
└── Story #126: 郵便物転送規約の信書規制対応 (Todo ID: 3)

Branch: ai/epic-123-legal-compliance-improvement
PR: Epic #123完了 - 契約書法的コンプライアンス改善
```

### ラベル体系

#### 種別ラベル
- `epic` - Epic
- `story` - Story
- `bug` - Bug Report
- `task` - Task
- `ai-proposal` - AI提案

#### 優先度ラベル
- `priority:critical` - 緊急（法的リスクあり）
- `priority:high` - 高
- `priority:medium` - 中
- `priority:low` - 低

#### 分野ラベル
- `legal:postal-law` - 郵便法関連
- `legal:aml` - 犯罪収益移転防止法関連
- `legal:privacy` - 個人情報保護法関連
- `legal:consumer` - 消費者契約法関連
- `legal:corporate` - 商法・会社法関連

#### 状態ラベル
- `needs-triage` - トリアージ待ち
- `needs-expert-review` - 専門家レビュー必要
- `needs-human-review` - 人間レビュー必要（AI提案用）
- `in-progress` - 作業中
- `blocked` - ブロック中
- `ready-for-review` - レビュー準備完了

#### 影響範囲ラベル
- `impact:critical` - 事業継続に関わる
- `impact:high` - 重要な機能に影響
- `impact:medium` - 一部機能に影響
- `impact:low` - 軽微な影響

### Issue作成ガイドライン

#### Epic作成時のポイント
1. **明確なビジネス価値**を記載する
2. **法的根拠**を明確にする
3. **完了条件**を具体的に定義する
4. **リスク評価**を含める
5. **専門家レビューの要否**を明記する

#### Story作成時のポイント
1. **ユーザーストーリー形式**で記載する
2. **受け入れ条件**を明確にする
3. **関連Epic**を必ず紐付ける
4. **作業サイズ**を適切に見積もる
5. **法的影響**があれば明記する

#### Bug Report作成時のポイント
1. **法的リスクレベル**を明確にする
2. **影響範囲**を具体的に記載する
3. **根拠法令**を明記する
4. **緊急度**を適切に設定する
5. **暫定回避策**があれば記載する

---

## 🔄 プルリクエスト

### PRの種類

#### 通常のPR（develop ← feature）
- **目的**: 機能追加、改善、修正
- **レビュー**: 最低1名
- **マージ**: Squash merge推奨

#### 重要なPR（main ← develop/release）
- **目的**: プロダクションリリース
- **レビュー**: 専門家レビュー必須
- **マージ**: Merge commit（履歴保持）

#### 緊急PR（main ← hotfix）
- **目的**: 緊急の法的問題対応
- **レビュー**: 専門家の緊急レビュー
- **マージ**: 迅速対応、後日詳細レビュー

### PRテンプレート

#### 基本情報
```markdown
## 📝 変更内容
[変更内容の概要を記載]

## 🎫 関連Issue
Closes #[issue番号]

## ⚖️ 法的影響
- [ ] 法的影響なし
- [ ] 軽微な法的影響（専門家レビュー不要）
- [ ] 重要な法的影響（専門家レビュー必要）
- [ ] 緊急の法的リスク対応

## ✅ チェックリスト
- [ ] 関連する契約書類の整合性を確認
- [ ] 法務チェックリストを確認
- [ ] リスク評価を更新（必要に応じて）
- [ ] ドキュメントを更新
- [ ] テストを実行（該当する場合）

## 🔍 レビューのポイント
[レビューしてほしい特定のポイントを記載]

## 📋 テスト内容
[実施したテスト内容を記載]
```

### レビュー基準

#### コードレビュー観点
1. **法的正確性**: 法令への適合性
2. **文書品質**: 誤字脱字、表現の適切性
3. **一貫性**: 他の文書との整合性
4. **完全性**: 必要な項目の網羅性
5. **リスク評価**: 潜在的リスクの特定

#### 専門家レビュー観点
1. **法令適合性**: 関連法令への完全な準拠
2. **実務適用性**: 実際の運用での妥当性
3. **リスク評価**: 法的リスクの適切な評価
4. **将来対応**: 法改正等への対応力
5. **業界標準**: 業界標準との比較

---

**最終更新**: 2025年8月18日  
**関連文書**: [プロジェクト概要](overview.md) | [法務コンプライアンス](legal-compliance.md) | [AI協働ガイド](ai-collaboration.md)