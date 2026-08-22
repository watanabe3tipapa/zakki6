# zakki6

> **v0.1.2** — メモ、参照用ノート、書籍目録をQuartoで公開する雑記録です。

[公開サイト](https://watanabe3tipapa.github.io/zakki6/) · [リポジトリ](https://github.com/watanabe3tipapa/zakki6) · [Actions](https://github.com/watanabe3tipapa/zakki6/actions)

## 概要

`zakki6` は、Quartoで公開する小さな雑記録サイトです。トップページは、公開済みコンテンツと運用情報への入口として機能します。各カードには対象ファイル、概要、リンクを表示し、メモや目録を見つけやすくしています。公開用HTMLはリポジトリに保存せず、GitHub Actions上でレンダリングします。

## コンテンツ

| ファイル／場所 | 内容 | 参照先 |
| --- | --- | --- |
| `index.qmd` | カード型LPです。書籍目録、OGPメモ、更新フロー、ソースへの導線を提供します。 | [公開ページ](https://watanabe3tipapa.github.io/zakki6/) |
| `books/BOOK_2024.qmd` | 機械学習・データ分析のための105冊をまとめた、サイト内で読める書籍目録です。 | [公開ページ](https://watanabe3tipapa.github.io/zakki6/books/BOOK_2024.html) |
| `notes/note01.qmd` | QuartoにおけるOGPタグ設定とGitHubリポジトリのOGP画像に関するメモです。 | [公開ページ](https://watanabe3tipapa.github.io/zakki6/notes/note01.html) |
| `assets/` | トップページとOGPで利用する画像アセットです。 | [ディレクトリ](assets/) |
| `_quarto.yml` | ナビゲーション、HTML出力、アセットの扱いを定義するQuarto設定です。 | [設定ファイル](_quarto.yml) |
| `.github/workflows/deploy-pages.yml` | 変更の選別、検査、レンダリング、GitHub Pages公開を行うワークフローです。 | [ワークフロー](.github/workflows/deploy-pages.yml) |

## クイックスタート

閲覧だけであれば、[公開サイト](https://watanabe3tipapa.github.io/zakki6/)を開いてください。ローカルで編集・確認する場合は、Quarto CLIを導入したうえで次を実行します。

```bash
git clone https://github.com/watanabe3tipapa/zakki6.git
cd zakki6
quarto preview
```

公開用HTMLを一度だけ生成する場合は、次のコマンドを実行します。

```bash
quarto render --to html
```

生成先は `_docs/` です。ここは公開成果物であり、通常はリポジトリにコミットしません。

## 更新フローと自動デプロイ

`.github/workflows/deploy-pages.yml` は、**`zakki6` の `main` ブランチへ明示的にPushされた変更**を対象に実行されます。ほかのリポジトリのPushを受け取る構成ではありません。GitHub Pagesの公開元はGitHub Actionsであり、ローカル生成物をPushする必要はありません。

| 段階 | 実行内容 | 結果 |
| --- | --- | --- |
| 変更の選別 | Push前後のファイル一覧を比較します。Quarto設定、`.qmd`、`books/`、`assets/`、スタイル、ワークフローなどのサイト影響ファイルだけを対象にします。 | 生成済みHTMLや補助生成物のみの変更はデプロイをスキップします。 |
| 差分検査 | 対象Pushの完全なコミット履歴を取得し、空白エラーを検査します。 | 問題があればビルド前に停止します。 |
| Quarto検証 | GitHub上でHTMLをレンダリングし、トップページの生成と診断メッセージを確認します。 | 警告・エラーがあれば公開しません。 |
| Pages公開 | 検査に成功した `_docs/` のみをGitHub Pagesへ配信します。 | 公開サイトが更新されます。 |

通常の更新は、`main` へPull Requestをマージすることで開始されます。変更の有無にかかわらず再ビルドしたい場合は、GitHub Actions画面から **Validate and deploy Quarto site** を手動実行してください。

## コンテンツを追加する場合

新しい公開ページは `.qmd` として追加してください。画像などの参照ファイルは、該当ページの近く、または `assets/` に置きます。新規ページを追加したら、`index.qmd` のカード一覧にリンク・対象ファイル・短い概要を追記してください。主要なページは、`_quarto.yml` のナビゲーションにも追加すると見つけやすくなります。

| 変更内容 | 実施すること |
| --- | --- |
| 新しいQuartoページ | `.qmd` を追加し、ページ先頭に正しいYAMLメタデータを記述します。`index.qmd` のカードと必要に応じて `_quarto.yml` のナビゲーションを更新します。 |
| 書籍・長文の資料 | `books/` に `.qmd` として配置し、タイトル、説明、カテゴリ、目次を設定します。ページへのリンクはトップページのカードから案内します。 |
| 画像・スタイル | `assets/` またはサイトで参照する場所に追加し、ローカルレンダリングでリンクと表示を確認します。 |
| 公開設定 | `_quarto.yml` または `.github/workflows/deploy-pages.yml` を変更した後、Actionsの実行結果と公開サイトを確認します。 |

## 開発・貢献

変更は作業ブランチで行い、Pull Requestを作成する前に `quarto render --to html` を実行してください。レンダリング後に `WARN`、`WARNING`、`ERROR` が出力されないことと、`_docs/index.html` および追加したページが生成されることを確認します。`main` への反映後、サイトに影響する変更だけが自動検査・デプロイの対象になります。

## ライセンス

このリポジトリには、現時点で明示的なライセンスファイルがありません。利用、再配布、または二次利用を検討する場合は、リポジトリ所有者に確認してください。
