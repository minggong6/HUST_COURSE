import os

repo_root = r"d:\coding\HUST_COURSE"
docs_root = r"d:\coding\HUST_COURSE\docs\source"

# Get repo folders
repo_folders = [f for f in os.listdir(repo_root) if os.path.isdir(os.path.join(repo_root, f))]
ignore_folders = {'.git', 'docs', 'guidebook', 'images', '_static', '_templates', '.idea', '.vscode'}
repo_folders = [f for f in repo_folders if f not in ignore_folders]

print(f"Found repo folders: {repo_folders}")

# Walk docs
for root, dirs, files in os.walk(docs_root):
    for file in files:
        if not file.endswith(".rst") or file == "index.rst" or file == "conf.py":
            continue
        
        course_name = os.path.splitext(file)[0]
        # Normalize for matching
        # Remove _ and spaces for comparison
        search_name = course_name.replace("_", "").replace(" ", "")
        
        match = None
        
        # Strategy 1: Exact match of filename to folder name
        if course_name in repo_folders:
            match = course_name
            
        # Strategy 2: Normalized match
        if not match:
            # Manual mappings
            manual_map = {
                "计算机与程序设计基础_C": "C语言",
                "信号与线性系统_二": "信号与系统",
                "复变函数与积分变换": "复变函数",
                "多媒体检索": "多媒体搜索"
            }
            if course_name in manual_map:
                match = manual_map[course_name]
            
            if not match:
                for folder in repo_folders:
                    if folder == course_name: 
                        match = folder
                        break
                    folder_norm = folder.replace("_", "").replace(" ", "")
                    if len(search_name) > 2 and len(folder_norm) > 2:
                        if search_name in folder_norm or folder_norm in search_name:
                            match = folder
                            break
        
        if match:
            print(f"Matched {file} -> {match}")
            
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            link = f"https://github.com/minggong6/HUST_COURSE/tree/main/{match}"
            link_rst = f"* `本课程 GitHub 仓库文件 <{link}>`_"
            
            if link in content:
                print(f"  Link already exists in {file}")
                continue
            
            # Find insertion point
            target_header = "复习资料\n--------"
            alt_header = "资料下载\n--------"
            
            if target_header in content:
                new_content = content.replace(target_header, f"{target_header}\n{link_rst}")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  Updated {file}")
            elif alt_header in content:
                new_content = content.replace(alt_header, f"{alt_header}\n{link_rst}")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  Updated {file} (using '资料下载')")
            else:
                print(f"  '复习资料' or '资料下载' section not found in {file}")
        else:
            # print(f"No match for {file}")
            pass
