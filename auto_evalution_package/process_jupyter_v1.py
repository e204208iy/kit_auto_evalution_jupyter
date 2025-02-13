import os
import re
import glob
import csv
import io
import nbformat
import numpy as np
from nbclient import NotebookClient
from PIL import Image, ImageChops
from typing import Tuple
import traceback

from auto_evalution_package.load_and_excute_notebook import extract_code_outputs

__all__ = ["evaluate_directory"]

def _load_and_execute_notebook(path: str) -> nbformat.NotebookNode:
    """Jupyter Notebook を読み込み、コードセルを実行する"""
    with open(path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)
    
    client = NotebookClient(notebook, kernel_name="python3")
    client.execute()
    
    return notebook


def _compare_code_outputs(submitted: str, answer: str) -> bool:
    """コード出力の比較（空白や改行を無視）"""
    return submitted.strip() == answer.strip()


def _compare_images(submitted_bytes: bytes, answer_bytes: bytes) -> bool:
    """画像の比較（ピクセル単位の差分チェック）"""
    submitted_img = Image.open(io.BytesIO(submitted_bytes))
    answer_img = Image.open(io.BytesIO(answer_bytes))

    if submitted_img.size != answer_img.size:
        return False

    diff = ImageChops.difference(submitted_img, answer_img)
    return np.sum(np.array(diff)) == 0


def _compare_notebooks(submitted_path: str, answer_path: str) -> Tuple[int, int]:
    """Notebook のコードセル出力を比較"""
    submitted_nb = _load_and_execute_notebook(submitted_path)
    answer_nb = _load_and_execute_notebook(answer_path)

    submitted_outputs = extract_code_outputs(submitted_nb)
    answer_outputs = extract_code_outputs(answer_nb)

    correct_count = 0
    total_count = len(answer_outputs)

    print(len(submitted_outputs))
    print(len(answer_outputs))

    for idx, (submitted, answer) in enumerate(zip(submitted_outputs, answer_outputs)):
        if answer[0] == "code":
            if _compare_code_outputs(submitted[1], answer[1]):
                correct_count += 1
            else:
                print(f"問題 {idx + 1} : ❌ コードが一致しません:\n[提出]: {submitted[1]}\n[正解]: {answer[1]}")
        
        elif answer[0] == "matplotlib":
            if _compare_images(submitted[1], answer[1]):
                correct_count += 1
            else:
                print(f"問題 {idx + 1} : ❌ 画像が一致しません")
        
        else:
            if submitted == answer:
                correct_count += 1
            else:
                print(f"問題 {idx + 1} : ❌ 出力が一致しません:\n[提出]: {submitted}\n[正解]: {answer}")

    return correct_count, total_count

def _extract_student_id(filename: str) -> str:
    """ファイル名から学籍番号を抽出（例: 242222_田中義昭.ipynb -> 242222）"""
    match = re.match(r"(\d{6})_", filename)
    return match.group(1) if match else filename

def evaluate_directory(submitted_dir: str, answer_path: str, output_csv: str):
    """ディレクトリ内の Notebook を評価し、結果を CSV に保存"""
    submitted_files = glob.glob(os.path.join(submitted_dir, "*.ipynb"))
    results = []

    for submitted_file in submitted_files:
        student_id = _extract_student_id(os.path.basename(submitted_file))
        
        try:
            correct, total = _compare_notebooks(submitted_file, answer_path)
            print(f"学籍番号 {student_id} : {correct}/{total}")
            results.append([student_id, correct])
        except Exception as e:
            print(f"エラー: {submitted_file} の評価中に問題が発生しました: {e}")
            traceback.print_exc()
            results.append([student_id, "エラー"])

    # CSVに保存
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["学籍番号", "点数"])
        writer.writerows(results)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Jupyter Notebook の提出物を評価")
    parser.add_argument("submitted_dir", help="提出された Notebook のディレクトリ")
    parser.add_argument("answer_path", help="正解の Notebook のパス")
    parser.add_argument("output_csv", help="評価結果を保存する CSV のパス")

    args = parser.parse_args()

    evaluate_directory(args.submitted_dir, args.answer_path, args.output_csv)