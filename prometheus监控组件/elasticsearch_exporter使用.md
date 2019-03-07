elasticsearch_exporter使用

>1 安装  
https://github.com/justwatchcom/elasticsearch_exporter/releases 下载安装包

tar -xvf elasticsearch_exporter-1.0.4rc1.linux-386.tar -C /usr/local/  

cd /usr/local

ln -s elasticsearch_exporter-1.0.4rc1.linux-386 elasticsearch_exporter

cd /usr/local/elasticsearch_exporter

./elasticsearch_exporter --web.listen-address "0.0.0.0:9109"  --es.uri http://elastic:changeme@localhost:9201

  
  
[root@bogon elasticsearch_exporter-1.0.4rc1.linux-386]# ./elasticsearch_exporter --help  
Usage of ./elasticsearch_exporter:  
  -es.all  
  &emsp;&emsp;Export stats for all nodes in the cluster. If used, this flag will override the flag es.node.  
  -es.ca string  
  &emsp;&emsp;Path to PEM file that contains trusted CAs for the Elasticsearch connection.  
  -es.client-cert string  
  &emsp;&emsp;Path to PEM file that contains the corresponding cert for the private key to connect to Elasticsearch.  
  -es.client-private-key string  
  &emsp;&emsp;Path to PEM file that contains the private key for client auth when connecting to Elasticsearch.  
  -es.indices  
  &emsp;&emsp;Export stats for indices in the cluster.  
  -es.node string  
  &emsp;&emsp;Node's name of which metrics should be exposed.  (default "_local")  
  -es.shards  
  &emsp;&emsp;Export stats for shards in the cluster (implies es.indices=true).  
  -es.ssl-skip-verify  
  &emsp;&emsp;Skip SSL verification when connecting to Elasticsearch.  
  -es.timeout duration  
  &emsp;&emsp;Timeout for trying to get stats from Elasticsearch. (default 5s)  
  -es.uri string  
  &emsp;&emsp;HTTP API address of an Elasticsearch node. (default "http://localhost:9200")  
  -log.format string  
  &emsp;&emsp;Sets the log format. Valid formats are json and logfmt (default "logfmt")  
  -log.level string  
  &emsp;&emsp;Sets the loglevel. Valid levels are debug, info, warn, error (default "info")  
  -log.output string  
  &emsp;&emsp;Sets the log output. Valid outputs are stdout and stderr (default "stdout")  
  -version  
  &emsp;&emsp;Show version and exit  
  -web.listen-address string  
  &emsp;&emsp;Address to listen on for web interface and telemetry. (default ":9108")  
  -web.telemetry-path string  
  &emsp;&emsp;Path under which to expose metrics. (default "/metrics")  