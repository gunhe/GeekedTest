# FROM python:3.14
FROM python:3.10-slim

# 安装 OpenCV 所需的系统库
# 安装 OpenCV 所需的系统库（适用于新版 Ubuntu/Debian）
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple  -r /code/requirements.txt

COPY . /code

CMD ["fastapi", "run", "app.py", "--port", "8080"]
# CMD ["python", "app.py", "--port", "8080"]
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]