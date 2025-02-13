import os

import csv
import nbformat
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

from pathlib import Path

def _load_notebook(path):
    """Jupyter Notebook を読み込む"""
    with open(path, encoding='utf-8') as f:
        return nbformat.read(f, as_version=4)

def _extract_problem_cells(notebook):
    """問題番号と対応するコードセルを抽出する"""
    problem_cells = {}
    
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            lines = cell['source'].split('\n')
            for line in lines:
                if line.startswith('#問題'):
                    problem_number = line.strip()
                    problem_cells[problem_number] = cell
                    break
    
    return problem_cells

def _extract_outputs(cell):
    """コードセルの出力を解析する"""
    outputs = []
    for output in cell.get('outputs', []):
        if 'text' in output:
            outputs.append(('text', output['text']))
        elif 'data' in output:
            if 'text/plain' in output['data']:
                outputs.append(('text', output['data']['text/plain']))
            if 'image/png' in output['data']:
                outputs.append(('image', output['data']['image/png']))
    return outputs

def _compare_outputs(correct_outputs, submitted_outputs):
    """出力の種類に応じた比較を行う"""
    if len(correct_outputs) != len(submitted_outputs):
        return False
    
    for (type1, data1), (type2, data2) in zip(correct_outputs, submitted_outputs):
        if type1 != type2:
            return False
        if type1 == 'text':
            if data1.strip() != data2.strip():
                return False
        elif type1 == 'image':
            img1 = Image.open(BytesIO(bytes(data1, 'utf-8')))
            img2 = Image.open(BytesIO(bytes(data2, 'utf-8')))
            if np.array_equal(np.array(img1), np.array(img2)) is False:
                return False
    
    return True

def grade_notebooks(correct_nb_path : str, submitted_dir : str):
    """正解Notebookと提出されたNotebookを比較し、結果をCSVに出力する"""
    correct_nb = _load_notebook(correct_nb_path)
    correct_cells = _extract_problem_cells(correct_nb)
    
    results = []
    
    for filename in os.listdir(submitted_dir):
        file_path = os.path.join(submitted_dir, filename)  # ここでフルパスを作成
        if filename.endswith('.ipynb') and os.path.isfile(file_path):  # ファイルのみを処理
            submitted_nb = _load_notebook(file_path)
            submitted_cells = _extract_problem_cells(submitted_nb)

            student_name = filename.replace('.ipynb', '')

            for problem, correct_cell in correct_cells.items():
                correct_outputs = _extract_outputs(correct_cell)
                submitted_outputs = _extract_outputs(submitted_cells.get(problem, {}))

                print(f"{student_name}を比較中...")
                score = _compare_outputs(correct_outputs, submitted_outputs)
                results.append([student_name, problem, score])
    
    with open('grading_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Student', 'Problem', 'Correct'])
        writer.writerows(results)
    
    print("Grading completed. Results saved to grading_results.csv")