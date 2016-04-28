## 安全策略

### 隐藏PHP版本号

编辑`php.ini`，应用`expose_php = Off`

### 隐藏php-fpm版本号

编辑`php-fpm.conf`，应用

```
fastcgi_param SERVER_SOFTWARE nginx/$nginx_version; 
改为： 
fastcgi_param SERVER_SOFTWARE nginx0.0.0; #(这个nginx0.0.0就是显示的内容)
```

### 隐藏Nginx版本号

编辑`nginx.conf`，在`http`应用

````
server_tokens off;
````

编辑`fastcgi_params`，应用

```
# fastcgi_param SERVER_SOFTWARE nginx/$nginx_version;
fastcgi_param SERVER_SOFTWARE nginx;
```

### 隐藏Apache版本号

编辑`httpd.conf`，应用

```
# ServerTokens OS
ServerTokens ProductOnly

# ServerSignature On
ServerSignature Off
```

## 监控

### 网络流量

```
sar -n DEV 1 100
```
