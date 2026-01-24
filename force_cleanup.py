#!/usr/bin/env python3
import os
import re
from pathlib import Path

docs_root = Path(r"d:\coding\HUST_COURSE\docs\source")

def cleanup_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. 移除特定的假链接和占位行
        patterns = [
            r"\* \*\*学分\*\*: 待补充\n",
            r"\* \*\*教材\*\*: 待补充\n",
            r"\* \*\*前置课程\*\*: 待补充\n",
            r"\* \*\*是否可以速通\*\*: \(例如：.*\n",
            r"\* \*\*速通建议\*\*: \(例如：.*\n",
            r"  \* \(例如：.*\n",
            r"\* \*\*推荐资源\*\*:\s*(?:`XX速成视频 <URL>`_)?\n",
            r"\* `XX速成视频 <URL>`_\n",
            r"\* `外部链接：学长整理的思维导图 \(GitHub\) <https://github\.com/xxxx>`_\n",
            r"\* :download:`2021-2022学年秋冬学期试卷 <\.\./\.\./downloads/xxx\.pdf>`\n",
            r"\* :download:`2020-2021学年秋冬学期试卷 <\.\./\.\./downloads/xxx\.pdf>`\n",
            r"\* :download:`课堂PPT合集 \(ZIP\) <\.\./\.\./downloads/xxx\.zip>`\n",
            r"\* “这门课主要靠背，理解不难。”\n",
            r"\* “期中考试很难，期末会调分。”\n",
            r"^\*?\s*\(在这里写学长学姐的主观评价，比如：\)\n",
            r"^\*?\s*\*\(在这里写学长学姐的主观评价，比如：\)\*\n",
            # 处理那种紧凑的错误
            r"复习资料\n--------\* :download:`课堂PPT合集 \(ZIP\) <\.\./\.\./downloads/xxx\.zip>`\n"
        ]
        
        for p in patterns:
            content = re.sub(p, "", content, flags=re.MULTILINE)

        # 2. 清理空的或只有冒号的标题项
        content = re.sub(r"\* \*\*速通建议\*\*:\s*\n", "", content)
        content = re.sub(r"\* \*\*推荐资源\*\*:\s*\n", "", content)

        # 3. 清理空章节
        # 如果一个章节后面直接跟着另一个章节标题或者文件结束，且中间只有空白，则删除该章节
        headers = ["基本信息", "速通指南", "课程评价", "历年试卷", "复习资料", "资料下载", "课程信息"]
        for header in headers:
            # 匹配 标题\n----\n(\s*)\n(下一个标题或结束)
            section_pattern = rf"{header}\n-+\n\s*(?=\n[^\-\n]+\n-+\n|\Z)"
            content = re.sub(section_pattern, "", content, flags=re.MULTILINE)

        # 4. 清理多余空行
        content = re.sub(r'\n\n\n+', '\n\n', content)
        content = content.strip() + '\n'

        if content != original and len(content) > 10:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error {filepath}: {e}")
        return False

def main():
    files = list(docs_root.rglob("*.rst"))
    count = 0
    for f in files:
        if cleanup_file(f):
            print(f"Cleaned {f.name}")
            count += 1
    print(f"Total cleaned: {count}")

if __name__ == "__main__":
    main()
