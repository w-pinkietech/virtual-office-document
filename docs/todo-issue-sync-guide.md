# Todo-Issue同期 実装ガイド

> **AI作業時のTodo-Issue完全同期システム**  
> 透明性・追跡可能性・効率性を実現する統合ワークフロー

## 🎯 概要

このガイドは、AI作業時にTodoとGitHub Issueを完全同期させ、プロジェクト管理の透明性と効率性を最大化するための実装方法を示します。

## 📋 基本原則

### 必須要件
1. **完全同期**: Todo ↔ Issue の双方向同期
2. **階層管理**: Epic → Story → Task の明確な階層
3. **進捗追跡**: リアルタイムでの進捗状況同期
4. **透明性**: 人間が常に全体状況を把握可能

### 同期マッピング
| Todo Level | GitHub Issue | 関係性 | 自動化 |
|------------|-------------|--------|--------|
| TodoWrite全体 | Epic | 1:1 | 自動作成 |
| 個別Todo | Story | 1:1 | 自動作成・同期 |
| Sub-task | Story Comment | 1:多 | 必要に応じて |

## 🔧 実装手順

### Phase 1: 環境準備

#### 1. GitHub CLI設定確認
```bash
# gh CLIの認証確認
gh auth status

# 必要に応じて認証
gh auth login
```

#### 2. テンプレート配置確認
```bash
# テンプレートファイルの存在確認
ls -la .github/templates/
# epic-ai-template.md
# story-ai-template.md
```

### Phase 2: Todo-Issue同期フロー

#### 1. TodoWrite実行と同時Epic作成
```bash
# 現在のTodo状況を分析
analyze_todos() {
    local todo_count=$(echo "$1" | jq '. | length')
    local epic_title="Epic: $(echo "$1" | jq -r '.[0].content' | sed 's/の.*/関連タスク/')"
    echo "Todo数: $todo_count, Epic名: $epic_title"
}

# Epic自動作成
create_epic_from_todos() {
    local todos="$1"
    local epic_title="$2"
    
    # Epic作成
    gh issue create \
        --title "$epic_title" \
        --body-file .github/templates/epic-ai-template.md \
        --label "epic,ai-proposal,priority:medium" \
        --assignee "@me"
    
    echo $? # Issue番号を返す
}
```

#### 2. 各TodoをStoryとして作成
```bash
# Story自動作成
create_stories_from_todos() {
    local todos="$1"
    local epic_number="$2"
    
    echo "$todos" | jq -c '.[]' | while read todo; do
        local todo_id=$(echo "$todo" | jq -r '.id')
        local todo_content=$(echo "$todo" | jq -r '.content')
        local story_title="Story: $todo_content"
        
        # Story作成
        gh issue create \
            --title "$story_title" \
            --body "Epic: #$epic_number
Todo ID: $todo_id

## 作業内容
$todo_content

## 受け入れ条件
- [ ] 作業完了
- [ ] 品質確認
- [ ] レビュー完了" \
            --label "story,ai-proposal" \
            --assignee "@me"
    done
}
```

#### 3. Todo状態変更時の自動Issue更新
```bash
# Todo状態同期
sync_todo_to_issue() {
    local todo_id="$1"
    local todo_status="$2"
    local issue_number="$3"
    
    case "$todo_status" in
        "pending")
            gh issue edit $issue_number --add-label "status:todo"
            ;;
        "in_progress")
            gh issue edit $issue_number --add-label "status:in-progress"
            gh issue comment $issue_number --body "🔄 作業開始: $(date)"
            ;;
        "completed")
            gh issue close $issue_number --comment "✅ Todo完了により自動クローズ: $(date)"
            gh issue edit $issue_number --add-label "status:completed"
            ;;
    esac
}
```

### Phase 3: 統合実装例

#### AI作業時の完全自動化スクリプト例
```bash
#!/bin/bash
# ai-todo-sync.sh - AI作業時のTodo-Issue完全同期

# 1. TodoWrite実行（AI）
execute_todo_write() {
    local task_description="$1"
    
    # TodoWriteを実行（実際のAI処理）
    # この部分は実際のTodoWrite APIコールに置き換え
    local todos='[
        {"id":"1","content":"個人情報保護方針の更新","status":"pending"},
        {"id":"2","content":"利用規約の消費者契約法適合","status":"pending"},
        {"id":"3","content":"郵便物転送規約の信書規制対応","status":"pending"}
    ]'
    
    echo "$todos"
}

# 2. Epic作成
create_epic() {
    local todos="$1"
    local epic_title="Epic: Todo-Issue同期システム実装"
    
    local epic_body="## 概要
AI作業時のTodo-Issue同期システムの実装

## 含まれるStories
$(echo "$todos" | jq -r '.[] | "- [ ] " + .content + " (Todo ID: " + .id + ")"')

## 完了条件
- [ ] すべてのStoriesが完了
- [ ] 同期システムが正常動作
- [ ] レビュー完了

## 法的影響度
Medium - システム改善、運用効率化"

    gh issue create \
        --title "$epic_title" \
        --body "$epic_body" \
        --label "epic,ai-proposal,priority:medium" \
        --assignee "@me" | grep -o '#[0-9]*' | sed 's/#//'
}

# 3. Stories作成
create_stories() {
    local todos="$1"
    local epic_number="$2"
    
    echo "$todos" | jq -c '.[]' | while read todo; do
        local todo_id=$(echo "$todo" | jq -r '.id')
        local todo_content=$(echo "$todo" | jq -r '.content')
        
        gh issue create \
            --title "Story: $todo_content" \
            --body "Epic: #$epic_number
Todo ID: $todo_id

## 作業内容
$todo_content

## 受け入れ条件
- [ ] 作業完了
- [ ] 品質確認
- [ ] レビュー完了" \
            --label "story,ai-proposal" \
            --assignee "@me"
    done
}

# 4. メイン実行フロー
main() {
    echo "🤖 AI作業開始: Todo-Issue同期"
    
    # TodoWrite実行
    local todos=$(execute_todo_write "Todo-Issue同期システム実装")
    echo "📋 Todo作成完了: $(echo "$todos" | jq '. | length')件"
    
    # Epic作成
    local epic_number=$(create_epic "$todos")
    echo "📊 Epic作成完了: #$epic_number"
    
    # Stories作成
    create_stories "$todos" "$epic_number"
    echo "📝 Stories作成完了"
    
    # 結果出力
    echo "
🤖 AI作業が完了しました。以下をご確認ください：

**Epic**: #$epic_number - Todo-Issue同期システム実装
**完了したStories**: 
$(gh issue list --label "epic:$epic_number" --json number,title --jq '.[] | "- #" + (.number | tostring) + " - " + .title')

**GitHubで確認**: 
- Epic: #$epic_number
- Stories: $(gh issue list --label "epic:$epic_number" --json number --jq '[.[] | "#" + (.number | tostring)] | join(", ")')

Epic全体とすべてのStoriesをレビューしていただき、問題なければマージの承認をお願いします。"
}

# 実行
main "$@"
```

## 🔍 実装チェックリスト

### セットアップ確認
- [ ] GitHub CLI認証済み
- [ ] テンプレートファイル配置済み
- [ ] ラベル体系設定済み
- [ ] 権限設定完了

### 動作確認
- [ ] TodoWrite → Epic作成の動作確認
- [ ] Epic → Stories作成の動作確認
- [ ] Todo状態変更 → Issue更新の確認
- [ ] 完了時のEpic Closeの確認

### 品質確認
- [ ] Epic-Story関連付けの正確性
- [ ] Todo IDとIssue Numberのマッピング
- [ ] 進捗同期の正確性
- [ ] 人間レビュープロセスの確保

## 🚨 注意事項

### 必須遵守事項
1. **人間承認**: 全ての作業は人間による最終承認が必要
2. **透明性**: 全ての変更がGitHubで追跡可能
3. **整合性**: Todo ↔ Issue の整合性を常に維持
4. **法的考慮**: 法的影響度に応じた適切なレビュー

### エラー処理
- Issue作成失敗時の再試行機能
- 同期エラー時の手動修正手順
- 整合性チェック機能の実装

## 📊 効果測定

### KPI
- Todo-Issue同期率: 100%維持
- 人間レビュー効率: 従来比50%向上
- プロジェクト透明性: 全作業のGitHub追跡
- エラー率: 5%以下

### 改善ポイント
- 自動化レベルの向上
- レビュー効率の最適化
- エラー処理の強化
- ユーザビリティの改善

---

**最終更新**: 2025年8月18日  
**関連文書**: [AI協働ガイド](ai-collaboration.md) | [Git運用ワークフロー](git-workflow.md)