监控redis
## 1.安装
>wget https://github.com/oliver006/redis_exporter/releases/download/v0.13/redis_exporter-v0.13.linux-amd64.tar.gz  
tar -xvf  redis_exporter-v0.13.linux-amd64.tar.gz -C /usr/local/sbin/

## 2.启动
> 无密码  
/usr/local/sbin/redis_exporter redis//127.0.0.1:6379 &  
有密码  
/usr/local/sbin/redis_exporter  -redis.addr 127.0.0.1:6379  -redis.password passwd   
redis_exporter -redis.addr 172.16.3.95:6379,172.16.3.101:6379

nohup redis_exporter -redis.addr 127.0.0.1:6379 -redis.alias test_102_redis -web.listen-address 0.0.0.0:16379 &>/tmp/test_102_redis.log &

## 3.验证
> 访问 http://172.16.24.197:9121/metrics

Usage of redis_exporter:  
  -check-keys string  
        Comma separated list of keys to export value and length/size  
  -debug  
        Output verbose debug information  
  -log-format string
        Log format, valid options are txt and json (default "txt")  
  -namespace string  
        Namespace for metrics (default "redis")  
  -redis.addr string  
        Address of one or more redis nodes, separated by separator  
  -redis.alias string  
        Redis instance alias for one or more redis nodes, separated by separator  
  -redis.file string  
        Path to file containing one or more redis nodes, separated by newline. NOTE: mutually exclusive with redis.addr  
  -redis.password string  
        Password for one or more redis nodes, separated by separator  
  -separator string  
        separator used to split redis.addr, redis.password and redis.alias into several elements. (default ",")
  -use-cf-bindings  
        Use Cloud Foundry service bindings  
  -version  
        Show version information and exit  
  -web.listen-address string  
        Address to listen on for web interface and telemetry. (default ":9121")  
  -web.telemetry-path string  
        Path under which to expose metrics. (default "/metrics")  