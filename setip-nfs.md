## Setup security groups

Protocol | Port(Service) | Source
---- | ---- | ----
TCP | 111 | 0.0.0.0/0
TCP | 2049 | 0.0.0.0/0
UDP | 111 | 0.0.0.0/0
UDP | 2049 | 0.0.0.0/0

## Server

### 创建用于共享数据的用户，客户端需要创建相同的用户，且保持id一致

```
/usr/sbin/groupadd www
/usr/sbin/useradd -r -g www www
```

### 安装nfs

```
yum install nfs-utils nfs-utils-lib
```

### 启动服务

```
chkconfig nfs on 
service rpcbind start
service nfs start
```

### 创建待共享的目录

```
mkdir -p /data/nfs/www.mo.com
chown -R www:www /data/nfs
```

### 添加导出配置

```
cat "/data/nfs/ 10.0.0.0/8(rw,sync,all_squash,anonuid=498,anongid=500)" >> /etc/exports
```

### 导出目录

```
exportfs -a
```

## Client

### 创建用于共享数据的用户，并保持和服务器端用户的id一致

```
/usr/sbin/groupadd www
/usr/sbin/useradd -r -g www www
```

### 安装nfs程序

```
yum -y install nfs-utils nfs-utils-lib
```

### 创建本地数据目录

```
mkdir -p /data/nfs/www.mo.com
```

### 挂载服务器端目录

```
mount -t nfs 192.168.0.21:/data/nfs/www.mo.com /data/nfs/www.mo.com
```

### 设置开机自动挂载

```
echo "192.168.0.21:/data/nfs/www.mo.com     /data/nfs/www.mo.com     nfs auto,noatime,nolock,bg,intr,tcp,actimeo=1800 0 0" >> /etc/fstab
mount -a
```
