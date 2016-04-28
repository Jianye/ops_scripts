## Setup MongoDB

### 安装

```
wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.4.9.tgz
tar xzf mongodb-linux-x86_64-2.4.9.tgz
cp -a mongodb-linux-x86_64-2.4.9 /usr/local/
ln -s /usr/local/mongodb-linux-x86_64-2.4.9 /usr/local/mongodb
```

### 创建目录

```
mkdir -p /etc/mongodb

mkdir -p /var/run/mongodb

mkdir -p /var/log/mongodb

mkdir -p /data/mongodb/27101
mkdir -p /data/mongodb/27102
mkdir -p /data/mongodb/27103

mkdir -p /data/mongodb/27201
mkdir -p /data/mongodb/27202
mkdir -p /data/mongodb/27203
```

### 配置文件

#### /etc/mongodb/27101.conf

```
port=27101

fork=true
logappend=true
directoryperdb=true
journal=true
quiet=true

logpath=/var/log/mongodb/27101.log
dbpath=/data/mongodb/27101/
pidfilepath=/var/run/mongodb/27101.pid
```

#### /etc/mongodb/27017.conf

```
port=27017

fork=true
logappend=true

configdb=127.0.0.1:27101
logpath=/var/log/mongodb/27017.log
pidfilepath=/var/run/mongodb/27017.pid
```

#### 启动服务器实例

```
# config #1
/usr/local/mongodb/bin/mongod -f /etc/mongodb/27101.conf 

# shard #1
/usr/local/mongodb/bin/mongod -f /etc/mongodb/27201.conf 

# shard #2
/usr/local/mongodb/bin/mongod -f /etc/mongodb/27202.conf 

# shard #3
/usr/local/mongodb/bin/mongod -f /etc/mongodb/27203.conf 

# mongos
/usr/local/mongodb/bin/mongos -f /etc/mongodb/27017.conf 

```

#### 账号安全

##### 创建一个管理员账号

```
use admin
db.addUser({user: "root", pwd: "root", roles: ["userAdmin", "userAdminAnyDatabase", "readWriteAnyDatabase", "clusterAdmin", "dbAdmin", "dbAdminAnyDatabase"]})
```

##### 创建一个只读账号

```
use admin
db.addUser("readonly", "readonly", true)
```

##### 关闭localhost无密码登录

```
/usr/local/mongodb/bin/mongod --setParameter enableLocalhostAuthBypass=0
```

##### 关闭服务

```
user admin
db.shutdownServer()
```

##### 创建Key File

```
openssl rand -base64 741 >/etc/mongodb/lol-match.key
chmod 600 /etc/mongodb/lol-match.key
```

### 针对LOL战绩做分片


#### 配置分片

```
/usr/local/mongodb/bin/mongo --port 27017

mongos> sh.addShard('127.0.0.1:27101')

mongos> sh.addShard('127.0.0.1:27102')

mongos> sh.addShard('127.0.0.1:27103')

mongos> sh.enableSharding('lol')

mongos> sh.shardCollection('lol.match', {"realm": 1, "gameid": 1})
```

#### 配置索引

```
mongos> db.match.ensureIndex({"realm": 1, "gameid": -1});

mongos> db.match.ensureIndex({"gamestarttime": -1})
```

## 生产环境配置

http://docs.mongodb.org/manual/administration/production-notes/

### 修改系统limit

http://docs.mongodb.org/manual/reference/ulimit/

```
ulimit -SHn 64000

$ vi /etc/security/limits.conf
* soft nofile 64000
* hard nofile 64000
* soft nproc 64000
* hard nproc 64000

$ vi /etc/security/limits.d/90-nproc.conf
* soft nproc 64000
* hard nproc 64000
```

### Read ahead settings

```
sudo blockdev --setra 32 /dev/xvdf

$ echo 'ACTION=="add", KERNEL=="xvdf", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules
```

### 软连接

```
mkdir -p /log/mongodb/27018 /log/mongodb/27019 /log/mongodb/27020
mkdir -p /journal/mongodb/27018 /journal/mongodb/27019 /journal/mongodb/27020
mkdir -p /data/mongodb/27018 /data/mongodb/27019 /data/mongodb/27020

ln -s /journal/mongodb/27018/ /data/mongodb/27018/journal
ln -s /journal/mongodb/27019/ /data/mongodb/27019/journal
ln -s /journal/mongodb/27020/ /data/mongodb/27020/journal

ln -s /usr/local/mongodb/bin/mongo* /usr/local/bin/
```

### 启动实例

```
/usr/local/mongodb/bin/mongod --configsvr --config /etc/mongodb/27019.conf
/usr/local/mongodb/bin/mongod --config /etc/mongodb/27020.conf
/usr/local/mongodb/bin/mongod --shardsvr --config /etc/mongodb/27018.conf

/usr/local/mongodb/bin/mongos --config /etc/mongodb/27017.conf
```

### 配置ReplSet实例

http://docs.mongodb.org/manual/tutorial/deploy-replica-set/

```
mongod -f /etc/mongodb/27018.conf

mongo
rs.initiate({"_id": "rs01-lol-mk", "members": [{"_id":0, "host": "db01.lol.mk:27018"}]})
rs.conf()
rs.addArb("arb01.lol.mk:27020")
rs.status()
```

### 配置Arbiter实例

http://docs.mongodb.org/manual/tutorial/add-replica-set-arbiter/

```
mongod -f /etc/mongodb/27020.conf

rs.addArb("m1.example.net:30000")
```

### 配置Shard实例

```
/usr/local/mongodb/bin/mongos --configdb cfg01.lol.mk:27019,cfg02.lol.mk:27019,cfg03.lol.mk:27019

/usr/local/mongodb/bin/mongo --host mongos01.lol.mk --port 27017
; Add shards
sh.addShard("rs01-lol-mk/db01.lol.mk:27018")
sh.addShard("rs02-lol-mk/db02.lol.mk:27018")
sh.addShard("rs03-lol-mk/db03.lol.mk:27018")
; Enable sharding
;db.runCommand({ enableSharding: "lol_br1" })
sh.enableSharding("lol_br1")
sh.enableSharding("lol_eun1")
sh.enableSharding("lol_euw1")
sh.enableSharding("lol_kr")
sh.enableSharding("lol_la1")
sh.enableSharding("lol_la2")
sh.enableSharding("lol_na1")
sh.enableSharding("lol_oc1")
sh.enableSharding("lol_ru")
sh.enableSharding("lol_tr1")
sh.enableSharding("lol_wt1")
; Shard collections
sh.shardCollection("lol_br1.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_eun1.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_euw1.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_kr.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_la1.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_la2.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_na1.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_oc1.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_ru.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_tr1.match", {"gamestarttime": 1, "_id": 1})
sh.shardCollection("lol_wt1.match", {"gamestarttime": 1, "_id": 1})
```

### 重置OpLog大小

http://docs.mongodb.org/manual/tutorial/change-oplog-size/

### 配置MMS

http://mms.mongodb.com/help/monitoring/#install-the-monitoring-agent-on-unix-linux

http://mms.mongodb.com/help/tutorial/install-monitoring-agent/
