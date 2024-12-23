# 基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /home/model_mall

# 将当前目录下的文件复制到镜像中
COPY . /home/model_mall

# 创建新用户
RUN useradd -ms /bin/bash model

# 切换到新用户
USER model

# 确保 ~/.local/bin 在 PATH 中
ENV PATH="/home/model/.local/bin:${PATH}"

# 安装项目依赖
COPY requirements.txt /home/model_mall
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 设置默认命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
