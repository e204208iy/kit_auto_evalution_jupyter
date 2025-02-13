# AI応用研究所 jupyter 自動採点プログラム
## 環境
- M2 mac book
- uv

# 使い方
```python
from auto_evalution_package import process_jupyter_v2

answer_path = "correct.ipynb"  # 正解ファイル（1つだけ）
submitted_dir = "merged_notebooks"  # 受験者のファイルがあるディレクトリ

# 評価を実行
process_jupyter_v2.grade_notebooks(answer_path,submitted_dir)
```
## 処理の大まかな流れ
1. 問題コメントがあるセルを抽出
2. セルのoutputを取得
3. outputの形式（int,numpy,matplotなど）に応じて評価を条件分岐
4. csvに結果をまとめる

## プロジェクトディレクトリの説明
1. org_notebook
   1. moodleから落としてきたnotebook群
2. scripts/
   1. folder_expansion.py
      1. moodleから落としてきた複数のフォルダを一つにまとめる機能
      2. org_notebook -> merged_notebooks
3. auto_evalution_package
   1. ジュピター自動採点のパッケージ
   2. process_jupyterモジュールがメインの処理

## 自動採点のための問題作成tips
- 変数を出力したいときはprint()を使う
- コードセルに「#問題X-Yのプログラム」というコメントを書き、評価対象のindexとする
- 

# 付録
## 生成AI プロンプト
目的 : jupyternotebookの自動採点プログラムを作ろうと思っています。
手法 : 正解のnotebookと提出されたnotebookを比較します。
評価方法 : 完全一致

以下問題例　２問　解答済み
```python
#問題1-2のプログラム
#最初の10行を表示
temp_data.head(10)
```
```python
#問題1-17のプログラム
import matplotlib.pyplot as plt

"""ここからコードを記述してください"""
plt.hist((y_test-y_pred)/y_test )
plt.xlabel('Error from predicted value')
plt.ylabel('frequency distribution')
plt.title("Histogram of difference between the correct value and the predicted value")
plt.grid(True)
```

****詳細設計****
1. コードセルに「#問題1-2のプログラム」のようにコメントが書いてあるセルを評価します。
2. 問題のセルのoutputにはさまざまな形式が含まれるため、種類によって評価を変えたいです。例えば,matplotlibであれば画像のピクセルが一致するかで評価、普通の出力であれば単純に正解のnotebookのoutputと比較します。
3. コードを評価する前に提出されたnotebookをrun allしてください。エラー行は無視してください。
4. 一つのipynbの処理が終わるごとに標準出力でxさんはy点でしたと表示してください。
5. 最後に結果をcsvにまとめてください(名前,問題名,Bool)。名前はファイル名から取得します。
6. モジュールとして実装し、正解のファイルのパスと提出されたnotebookのディレクトリのパスを渡します。
7. 複数のnotebookに対応したいです。
8. 仕様の変更や問題の変更に強い設計にしてください。
9. モジュール内でしか使わない関数には関数名の先頭に_をつけてください。
**************