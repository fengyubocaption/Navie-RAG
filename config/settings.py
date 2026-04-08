import os
from pathlib import Path

# 获取 settings.py 的爷爷目录，即项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 拼接出绝对路径
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_DIR = os.path.join(BASE_DIR, "file")
