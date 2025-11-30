import os

base_dir = r"d:\coding\HUST_COURSE\docs\source"

# 要插入的新内容
new_section = """
速通指南
--------
* **是否可以速通**: (例如：是，考前突击3天即可 / 否，需平时积累)
* **速通建议**: 
  * (例如：重点复习第三章，放弃第五章推导)
* **推荐资源**: 
  * `XX速成视频 <URL>`_
"""

# 遍历目录
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".rst") and file != "index.rst" and file != "conf.py":
            file_path = os.path.join(root, file)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 检查是否已经包含“速通指南”
            if "速通指南" in content:
                print(f"Skipping {file}: Already has 速通指南")
                continue
            
            # 查找插入点：在“课程评价”之前插入
            target_str = "课程评价\n--------"
            if target_str in content:
                new_content = content.replace(target_str, new_section + "\n" + target_str)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file}")
            else:
                print(f"Skipping {file}: Could not find insertion point '课程评价'")
