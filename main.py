from auto_evalution_package import process_jupyter_v2

# === 使い方 ===
submitted_dir = "merged_notebooks"  # 受験者のファイルがあるディレクトリ
answer_path = "correct.ipynb"  # 正解ファイル（1つだけ）

# 評価を実行
process_jupyter_v2.grade_notebooks(answer_path,submitted_dir)