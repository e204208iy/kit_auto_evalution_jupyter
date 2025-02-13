import re
import base64
from typing import List, Tuple, Union

import nbformat

# v3 画像自体をピクセルで比較するバージョン
def extract_code_outputs(notebook: nbformat.NotebookNode)-> List[Tuple[str, Union[str, bytes]]]:
    """Notebook から特定のコメントを含むコードセルの出力を抽出"""
    outputs = []
    #辞書の形式 -> 問題名 : 評価基準 問題数37 - 2 = 35
    comment_patterns = {
        "#問題1-1のプログラム": "output",
        "#問題1-2のプログラム": "output",
        "#問題1-3のプログラム": "code",
        "#問題1-4のプログラム": "output",
        "#問題1-5のプログラム": "output",
        "#問題1-6のプログラム": "output",
        "#問題1-7のプログラム": "output",
        "#問題1-8のプログラム": "output",
        "#問題1-9のプログラム": "output",
        "#問題1-10のプログラム": "output",
        "#問題1-11のプログラム": "output",
        "#問題1-12のプログラム": "output",
        "#問題1-13のプログラム": "output",
        "#問題1-14のプログラム": "output",
        "#問題1-15のプログラム": "output",
        "#問題1-16のプログラム": "output",
        "#問題1-17のプログラム": "matplotlib",
        "#問題1-18のプログラム": "matplotlib",
        "#問題2-1のプログラム": "output",
        "#問題2-2のプログラム": "code",
        "#問題2-3のプログラム": "output",
        "#問題2-4のプログラム": "output",
        "#問題2-5のプログラム": "code",
        "#問題2-6のプログラム": "output",
        "#問題2-7のプログラム": "output",
        "#問題2-8のプログラム": "output",
        "#問題2-9のプログラム": "output",
        "#問題2-10のプログラム": "output",
        "#問題2-11のプログラム": "output",
        "#問題2-12のプログラム": "output",
        "#問題2-13のプログラム": "output",
        # "#問題2-14のプログラム": "output",
        "#問題2-15のプログラム": "output",
        "#問題2-16のプログラム": "output",
        "#問題2-17のプログラム": "output",
        # "#問題2-18のプログラム": "output",
        "#問題3-1のプログラム": "output",
        "#問題3-2のプログラム": "output",
        "#問題3-3のプログラム": "output",
        "#問題3-4のプログラム": "output",
        "#問題3-5のプログラム": "matplotlib",
    }

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            code = "".join(cell['source'])
            matched_pattern = next((pattern for pattern in comment_patterns if pattern in code), None)

            if matched_pattern:
                evaluation_type = comment_patterns[matched_pattern]

                if evaluation_type == "output":
                    cell_outputs = []
                    for output in cell.get('outputs', []):
                        if 'text' in output:
                            cell_outputs.append(output['text'])
                        elif 'data' in output:
                            if 'text/plain' in output['data']:
                                cell_outputs.append(output['data']['text/plain'])
                            elif 'image/png' in output['data']:  # Matplotlib 画像出力の処理
                                image_data = base64.b64decode(output['data']['image/png'])  
                                cell_outputs.append(("matplotlib", image_data))
                        elif output.get('output_type') == 'error':
                            error_message = f"Error: {output['ename']}: {output['evalue']}"
                            if 'traceback' in output:
                                error_message += "\nTraceback:\n" + "\n".join(output['traceback'])
                            cell_outputs.append(error_message)

                    # 出力がない場合、空文字列を追加
                    if not cell_outputs:
                        outputs.append("")
                    else:
                        outputs.extend(cell_outputs)

                elif evaluation_type == "code":
                    # コード内容を正規化（空白や改行を無視）
                    normalized_code = re.sub(r'\s+', ' ', code).strip()
                    outputs.append(("code", normalized_code))
    return outputs