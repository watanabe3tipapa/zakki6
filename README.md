# zakki6

> **v0.1.2** — メモ、リンク、参照用ドキュメントを収めた雑記録です。

[公開サイト](https://watanabe3tipapa.github.io/zakki6/) · [リポジトリ](https://github.com/watanabe3tipapa/zakki6)

## 概要

`zakki6` は、Quartoで公開する小さな雑記録サイトです。トップページはコンテンツへの入口として機能し、各ファイルへのリンクと短い説明をカード形式で案内します。メモや目録はリポジトリで管理し、公開用のHTMLはGitHub上でレンダリングします。

## コンテンツ

| ファイル／場所 | 内容 | 参照先 |
| --- | --- | --- |
| `index.qmd` | サイトのトップページです。既存コンテンツへのリンクをカード形式で掲載します。 | [公開ページ](https://watanabe3tipapa.github.io/zakki6/) |
| `notes/note01.qmd` | QuartoにおけるOGPタグ設定とGitHubリポジトリのOGP画像に関するメモです。 | [公開ページ](https://watanabe3tipapa.github.io/zakki6/notes/note01.html) |
| `books/BOOK_2024.md` | 機械学習・データ分析に関する105冊の書籍目録です。 | [ソースファイル](books/BOOK_2024.md) |
| `assets/` | トップページとOGPで利用する画像アセットです。 | [ディレクトリ](assets/) |
| `_quarto.yml` | ナビゲーション、HTML出力、アセットの扱いを定義するQuarto設定です。 | [設定ファイル](_quarto.yml) |

## クイックスタート

閲覧だけであれば、[公開サイト](https://watanabe3tipapa.github.io/zakki6/)を開いてください。ローカルで編集・確認する場合は、Quarto CLIを導入したうえで次を実行します。

```bash
git clone https://github.com/watanabe3tipapa/zakki6.git
cd zakki6
quarto preview
```

公開用HTMLのみを生成する場合は、次のコマンドを使用します。

```bash
quarto render --to html
```

生成先は `_docs/` です。このディレクトリは公開成果物であり、通常はリポジトリへコミットしません。

## 自動検査とデプロイ

`.github/workflows/deploy-pages.yml` は、**`zakki6` の `main` ブランチへ明示的にPushされた変更**を対象に実行されます。ほかのリポジトリのPushを受け取る構成ではありません。

変更されたファイルを比較し、Quarto設定、`*.qmd`、`books/`、`assets/`、サイト用のスタイルや依存ファイル、デプロイワークフロー自体など、サイトに影響する変更だけを対象にします。生成済みのHTMLや補助生成物だけが変更された場合は、デプロイをスキップします。

対象となった場合は、GitHub Actions上で次の順に処理します。

1. 変更差分の空白エラーを検査します。
2. QuartoでHTMLをレンダリングし、`_docs/index.html` の生成と診断メッセージを確認します。
3. 検査に成功した成果物のみをGitHub Pagesへデプロイします。

GitHub上の環境で処理するため、ローカルで生成した `_docs/` をPushする必要はありません。必要に応じて、Actions画面から手動実行することもできます。

## コンテンツを追加する場合

新しいメモは、Quartoで公開する場合は `.qmd` として追加してください。画像などの参照ファイルは、該当するコンテンツの近くまたは `assets/` に置きます。追加後は `index.qmd` のカード一覧にもリンクと短い概要を追記すると、公開サイトから見つけやすくなります。

| 変更内容 | 実施すること |
| --- | --- |
| 新しいQuartoページ | `.qmd` を追加し、`index.qmd` のカードと必要に応じて `_quarto.yml` のナビゲーションを更新します。 |
| 画像・スタイル | `assets/` またはサイトで参照する場所へ追加し、リンク切れがないことを確認します。 |
| Markdownの資料 | リポジトリで参照する場合は `books/` などに配置し、トップページのカードから案内します。 |
| 公開設定 | `_quarto.yml` または `.github/workflows/deploy-pages.yml` を変更した後、Actionsの実行結果を確認します。 |

## 開発・貢献

変更は作業ブランチで行い、Quartoレンダリングを確認したうえでPull Requestを作成してください。`main` への反映後、サイト影響ファイルの変更だけが自動検査・デプロイの対象になります。

## ライセンス

このリポジトリには、現時点で明示的なライセンスファイルがありません。利用、再配布、または二次利用を検討する場合は、リポジトリ所有者に確認してください。
