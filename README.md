# ttdsCW3

1. 安装MySQL，解压文件并放到安装目录里：https://dev.mysql.com/downloads/mysql/
2. 配置PATH环境变量

```
<INSTALL_DIR>/bin
```

3. 在安装目录下创建my.ini配置文件，写入：（把basedir和datadir改成自己的）

```
[client]
# 设置mysql客户端默认字符集
default-character-set=utf8
 
[mysqld]
# 设置3306端口
port = 3306
# 设置mysql的安装目录
basedir=D:\\MySQL\\mysql-8.0.23-winx64
# 设置 mysql数据库的数据的存放目录，MySQL 8+ 不需要以下配置，系统自己生成即可，否则有可能报错
# datadir=D:\\MySQL\\data
# 允许最大连接数
max_connections=20
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
```

4. 管理员权限打开命令行，初始化

```
mysqld --initialize --console
```

记住最后给的随机初始化的密码

5. 安装，然后启动：

```
mysqld install
net start mysql
```

6. 登录，改密码，关闭服务：

```
mysql -h localhost -u root -p
alter user 'root'@'localhost' identified by '1301410442';
net stop mysql
```

7. 导入sql script

```
create database imdb_ttds;
mysql –u root -D imdb_ttds -p < xxxx.sql
```

