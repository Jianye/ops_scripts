## Setup PHP

### 安装依赖库

```
yum install -y autoconf automake libtool libicu-devel libmcrypt-devel mysql-devel
```

### 下载编译

```
tar xzf php-5.5.10.tar.gz
cd php-5.5.10
./configure  --prefix=/usr/local/php-5.5.10 --enable-exif --enable-fpm --enable-mbstring --with-config-file-path=/etc/php --with-freetype-dir --with-gd --with-jpeg-dir --with-png-dir --with-iconv-dir --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --with-zlib --with-curl --enable-intl --with-icu-dir=/usr --with-fpm-user=www --with-fpm-group=www --with-libxml-dir --disable-rpath --enable-bcmath --enable-shmop --enable-sysvsem --with-mcrypt --enable-mbregex --with-openssl --enable-soap --enable-gd-native-ttf --enable-ftp --enable-pcntl --enable-sockets --with-xmlrpc --enable-zip --enable-calendar --with-bz2 --with-gettext --enable-wddx
make
sudo make install
ln -s /usr/local/php-5.5.10 /usr/local/php

```
