import os
import shutil

def rename_png_files(directory):
    # 路径到包含PNG文件的文件夹
    path = os.path.join(directory, 'Results')
    
    # 获取所有png文件并按名称排序
    files = [f for f in os.listdir(path) if f.endswith('.png')]
    files.sort()
    index = 0
    # 重命名文件
    for _,file in enumerate(files):
        # 构建新文件名
        index += 1
        new_filename = f"{index}.png"
        # 源文件完整路径
        old_file = os.path.join(path, file)
        # 新文件完整路径
        new_file = os.path.join(path, new_filename)
        # 重命名文件
        shutil.move(old_file, new_file)
        print(f"Renamed '{file}' to '{new_filename}'")

# 使用函数，'your_directory_path'是你的文件夹的路径，比如'/home/user/documents'
rename_png_files('D:\Research\Chem_Structure')
