import os

base_dir = r"d:\coding\HUST_COURSE\docs\source"

categories = {
    "ideological_politics": {
        "title": "思政课程",
        "courses": [
            "思想道德与法治", "形势与政策", "中国近现代史纲要", "马克思主义基本原理",
            "习近平新时代中国特色社会主义思想概论", "毛泽东思想和中国特色社会主义理论体系概论"
        ]
    },
    "public_elective": {
        "title": "公选课程",
        "courses": ["素质教育选修课"]
    },
    "professional_elective": {
        "title": "专业选修课程",
        "courses": [
            "Java语言程序设计", "Xilinx_FPGA及应用", "MSP430单片机及应用", "Freescale单片机及应用",
            "8051系列单片机原理及应用", "Python编程技术", "数据库及应用实践", "操作系统",
            "DSP处理器及应用", "嵌入式_Linux软件设计", "虚拟仪器技术及应用", "传感器技术及应用",
            "数字图像处理", "现代网络技术", "网络与信息安全", "软件无线电", "绿色通信技术导论",
            "物联网", "微波射频电路", "天线与电波传播", "机器学习", "卫星通信原理", "医学图像处理",
            "应用密码学", "深度学习与计算机视觉", "多媒体检索", "定位与导航技术", "卫星通信系统",
            "高维信号处理", "智能通信", "移动通信网络", "通信编码理论", "移动通信系统设计和实验",
            "智能通信系统设计和实验", "空间通信系统设计和实验", "网络系统设计和实验"
        ]
    },
    "science": {
        "title": "理学课程",
        "courses": [
            "微积分_B_上", "微积分_B_下", "线性代数_B", "概率论与数理统计_B",
            "大学物理_A_上", "大学物理_A_下", "物理实验_上", "物理实验_下",
            "复变函数与积分变换", "数理方程与特殊函数", "随机过程"
        ]
    },
    "electrical": {
        "title": "电学课程",
        "courses": [
            "电路理论_三", "电路测试实验", "模拟电子技术_二", "数字电子技术",
            "电子线路设计_测试及实验_一", "电子线路设计_测试及实验_二",
            "电磁场与电磁波_二", "微波技术基础_二", "通信电子线路", "微机原理", "微机原理实验"
        ]
    },
    "information": {
        "title": "信息类课程",
        "courses": [
            "计算机与程序设计基础_C", "信息技术导论", "数据结构", "信号与线性系统_二",
            "基础信息论", "计算机网络", "数字信号处理", "通信原理_一", "无线通信基础"
        ]
    }
}

template = """{course_name}
======================

基本信息
--------
* **学分**: 待补充
* **教材**: 待补充
* **前置课程**: 待补充

速通指南
--------
* **是否可以速通**: (例如：是，考前突击3天即可 / 否，需平时积累)
* **速通建议**: 
  * (例如：重点复习第三章，放弃第五章推导)
* **推荐资源**: 
  * `XX速成视频 <URL>`_

课程评价
--------
*(在这里写学长学姐的主观评价，比如：)*
* “这门课主要靠背，理解不难。”
* “期中考试很难，期末会调分。”

历年试卷
--------
* :download:`2021-2022学年秋冬学期试卷 <../../downloads/xxx.pdf>`
* :download:`2020-2021学年秋冬学期试卷 <../../downloads/xxx.pdf>`

复习资料
--------
* `外部链接：学长整理的思维导图 (GitHub) <https://github.com/xxxx>`_
* :download:`课堂PPT合集 (ZIP) <../../downloads/xxx.zip>`
"""

index_template = """{title}
{underline}

.. toctree::
   :maxdepth: 2
   :caption: {title}

{toc_entries}
"""

def create_files():
    for cat_key, cat_data in categories.items():
        cat_dir = os.path.join(base_dir, cat_key)
        os.makedirs(cat_dir, exist_ok=True)
        
        toc_entries = ""
        for course in cat_data["courses"]:
            # Replace spaces/special chars for filename
            filename = course.replace(" ", "_").replace("（", "_").replace("）", "").replace("(", "_").replace(")", "")
            file_path = os.path.join(cat_dir, f"{filename}.rst")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(template.format(course_name=course))
            
            toc_entries += f"   {filename}\n"
            
        # Create index.rst
        index_path = os.path.join(cat_dir, "index.rst")
        title = cat_data["title"]
        # Calculate underline length based on byte length for utf-8 characters roughly, or just make it long enough
        underline = "=" * 30 
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_template.format(title=title, underline=underline, toc_entries=toc_entries))
            
        print(f"Created {cat_key} with {len(cat_data['courses'])} courses.")

if __name__ == "__main__":
    create_files()
