
FROM ubuntu:16.04

MAINTAINER kagxin
# 更换为国内镜像源
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	libmysqlclient-dev \
	locales \
	tzdata \
	nginx \
	supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*

# system set character utf8
RUN locale-gen zh_CN && \
	locale-gen zh_CN.utf8 && \
	update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 LANGUAGE=zh_CN.UTF-8

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

# 修改时区
RUN rm /etc/localtime && \
    ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# install uwsgi now because it takes a little while
RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com uwsgi


# mysql container and redis container alias
ENV mysqlhost=mysqldb
ENV redishost=redisdb

# setup all the configfiles
COPY supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
COPY requirements.txt /home/docker/code/

# 使用国内镜像源
RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -r /home/docker/code/requirements.txt

# add (the rest of) our code
COPY . /home/docker/code/

# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
EXPOSE 8000
CMD ["supervisord", "-n"]