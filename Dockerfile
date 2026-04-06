# 1. 基础镜像：使用官方轻量级的 Python 3.10
FROM python:3.10-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 先把依赖清单拷进去（利用 Docker 缓存机制，只要依赖没变，这步极快）
COPY requirements.txt .

# 4. 安装依赖
# 换成阿里云镜像源，并增加超时时间到 100s
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 5. 把你写的全部代码文件拷贝到容器的 /app 目录下
COPY . .

# 6. 声明容器要暴露的端口（和 FastAPI 保持一致）
EXPOSE 8000

# 7. 启动命令：使用 uvicorn 启动应用，注意 host 必须是 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]