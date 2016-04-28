### 编译安装node.Js-v0.10.32
```
mkdir /root/source
cd /root/source
wget http://nodejs.org/dist/v0.10.32/node-v0.10.32.tar.gz
tar -zxf node-v0.10.32.tar.gz
cd node-v0.10.32
./configure  --prefix=/usr/local/node-v0.10.32
make && make install
ln -s /usr/local/node-v0.10.32 /usr/local/node
ln -s /usr/local/node/bin/* /usr/bin/
```
