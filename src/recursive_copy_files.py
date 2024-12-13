import os
import shutil

def copy_contents_recursively(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    entries = os.listdir(source_dir_path)
    for file in entries:
        from_path = os.path.join(source_dir_path, file)
        dest_path = os.path.join(dest_dir_path, file)
        print(f"from: {from_path} --> to: {dest_path}")

        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_contents_recursively(from_path, dest_path)
