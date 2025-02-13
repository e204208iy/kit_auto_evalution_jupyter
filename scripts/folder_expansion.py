import os
import shutil

# 元のフォルダと移動先フォルダの指定
source_dir = "org_notebook"
dest_dir = "merged_notebooks"

# 移動先フォルダを作成（存在しない場合）
os.makedirs(dest_dir, exist_ok=True)

# フォルダを走査
for folder in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder)

    # フォルダかどうか確認
    if os.path.isdir(folder_path):
        # フォルダ名をスペース区切りで分割
        parts = folder.split(" ")
        if len(parts) >= 2:
            new_filename_prefix = f"{parts[0]} {parts[1]}"  # 例: "244124 堤 良太"

            # フォルダ内のファイルを確認
            for file in os.listdir(folder_path):
                if file.endswith(".ipynb"):
                    old_filepath = os.path.join(folder_path, file)
                    new_filename = f"{new_filename_prefix}.ipynb"
                    new_filepath = os.path.join(dest_dir, new_filename)

                    # ファイルを移動
                    shutil.move(old_filepath, new_filepath)
                    print(f"Moved: {old_filepath} -> {new_filepath}")

print("すべてのファイルを移動しました。")

