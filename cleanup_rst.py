#!/usr/bin/env python3
"""
清理docs/source下所有rst文件中的无用链接和框架内容
保留：
1. 有实际内容的部分（有真实链接和内容填充的部分）
2. 有用的导航链接
删除：
1. 占位符内容（待补充、例如、URL等）
2. 假链接（github/xxxx, downloads/xxx.pdf等）
3. 未完成的框架模板
"""

import os
import re
from pathlib import Path

docs_root = Path(r"d:\coding\HUST_COURSE\docs\source")

# 需要清理的模式
patterns_to_remove = [
    # 占位符
    r".*待补充.*\n",
    r".*\(例如：.*\)\n",
    r".*\*\*是否可以速通\*\*.*\(例如：.*\n",
    r".*\*\*速通建议\*\*.*\n\s+\*.*\(例如：.*\n",
    # 针对新发现的空项
    r"\* \*\*速通建议\*\*:\s*\n",
    r"\* \*\*推荐资源\*\*:\s*\n",
    # 针对课程评价的模板内容
    r"^\*?\s*\(\s*(在这里写学长学姐的主观评价，比如：\s*\)\s*\n",
    r"^\*?\s*“这门课主要靠背，理解不难。”\s*\n",
    r"^\*?\s*“期中考试很难，期末会调分。”\s*\n",
    r"^\*?\s*\*\(在这里写学长学姐的主观评价，比如：\*\)\s*\n",
    # 针对假连接
    r"^\s*\*\s*`XX速成视频\s*<URL>`_\n",
    r"^\s*\*\s*`外部链接：学长整理的思维导图\s*\(GitHub\)\s*<https://github\.com/xxxx>`_\n",
    r"^\s*\*\s*`HUST-Network-Login\s*<https://github\.com/xxxx>`_\n",
    # 假下载链接
    r"^\s*\*\s*:download:`2021-2022学年秋冬学期试卷 <\.\./\.\./downloads/xxx\.pdf>`\n",
    r"^\s*\*\s*:download:`2020-2021学年秋冬学期试卷 <\.\./\.\./downloads/xxx\.pdf>`\n",
    r"^\s*\*\s*:download:`课堂PPT合集 \(ZIP\) <\.\./\.\./downloads/xxx\.zip>`\n",
    # 复习资料下的紧凑型假连接
    r"复习资料\n--------\* :download:`课堂PPT合集 \(ZIP\) <\.\./\.\./downloads/xxx\.zip>`\n",
]

# 需要按顺序清理的空标题部分
def cleanup_empty_sections(content):
    # 定义标题及其装饰线
    sections = ["基本信息", "速通指南", "课程评价", "历年试卷", "复习资料", "资料下载", "课程信息"]
    # 循环多次以处理连续的空标题
    for _ in range(3):
        for section in sections:
            # 匹配标题行和装饰线行，如果后面只跟着空白字符且紧接着另一个标题或者文件结束，就删除
            pattern = rf"^{section}\n-+\n+(?=(?:{'|'.join(sections)})|$)"
            content = re.sub(pattern, "", content, flags=re.MULTILINE)
    return content

def cleanup_file(filepath):
    """清理单个rst文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用正则替换
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # 清除空的部分
        content = cleanup_empty_sections(content)
        
        # 清理多余的空行和省略号
        content = re.sub(r'^\.\.\.\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # 删除末尾的多余空行
        content = content.rstrip() + '\n'
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """主函数"""
    rst_files = list(docs_root.rglob("*.rst"))
    # 只处理docs/source下的文件（排除子目录里的临时文件等）
    rst_files = [f for f in rst_files if "runs" not in str(f)]
    
    print(f"Found {len(rst_files)} rst files to process")
    
    modified_count = 0
    for filepath in sorted(rst_files):
        if cleanup_file(filepath):
            modified_count += 1
            print(f"✓ Cleaned: {filepath.relative_to(docs_root.parent)}")
        else:
            print(f"- Skipped: {filepath.relative_to(docs_root.parent)}")
    
    print(f"\nCleaned {modified_count} files")

if __name__ == "__main__":
    main()
