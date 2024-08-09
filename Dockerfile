# 使用官方Python镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的/app目录
COPY . /app

# 安装Python依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 指定启动命令
CMD ["python", "bot.py"]
