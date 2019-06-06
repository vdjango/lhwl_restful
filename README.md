## py环境

```
rpm -ivh http://mirrors.ustc.edu.cn/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -ivh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

sudo yum install epel-release
sudo yum makecache
sudo yum groupinstall "Development Tools"
sudo yum install python<version>
sudo yum install python<version>-devel nginx
sudo setenforce 0
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --reload
or
sudo iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
wget https://bootstrap.pypa.io/get-pip.py
python<version> get-pip.py
```

## py扩展

```
pip<version> install -r .\requirement.txt
pip<version> install uwsgi
uwsgi --ini /lhwil/uwsgi.ini
```


## 创建数据库

CREATE DATABASE lhwill DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

### [Bug 调试]： 关于数据迁移失败问题

python manage.py makemigrations --merge


## uwsgi 部署问题

导入 lhwill/__init__.py

```
import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')
sys.path.append('/usr/local/lib64/python3.6/site-packages')
import pymysql
pymysql.install_as_MySQLdb()
```

## 生成索引

python manage.py rebuild_index

创建 uwsgi.ini 配置文件

```

[uwsgi]
// 启动uwsgi的用户名和用户组
uid=uwsgi
gid=uwsgi
// 指定IP端口
http=0.0.0.0:8080
// 项目目录
chdir=/home/lhwill/
// 指定静态文件
static-map=/static=/home/lhwill/static
//// 下面一般不需要修改 ////
// 指定sock的文件路径
socket=/home/uwsgi.sock
pidfile=/home/uwsgi.pid
// 设置日志目录
daemonize=/home/uwsgi.log
// 启用主进程
master=true
// 自动移除unix Socket和pid文件当服务停止的时候
vacuum=true
// 序列化接受的内容，如果可能的话
thunder-lock=true
// 启用线程
enable-threads=true
// 设置自中断时间
harakiri=30
// 设置缓冲
post-buffering=4096
// 进程个数
workers=5
// 指定项目的application
module=lhwill.wsgi:application
```

