postgresql_exports使用

>1 安装  
go get github.com/wrouesnel/postgres_exporter （yum install go -y）  
[root@sipcloud-monitor src]# go get github.com/wrouesnel/postgres_exporter
package github.com/wrouesnel/postgres_exporter: build constraints exclude all Go files in /root/go/src/github.com/wrouesnel/postgres_exporter           
[root@sipcloud-monitor src]# ls /root/go/src/github.com/wrouesnel/postgres_exporter  
cmd         gh-assets-clone.sh  LICENSE      mage.go                                    postgres_exporter.rc             queries.yaml  tools
Dockerfile  gh-metrics-push.sh  magefile.go  postgres_exporter_integration_test_script  postgres-metrics-get-changes.sh  README.md     vendor
[root@sipcloud-monitor src]# 

cd /root/go/src/github.com/wrouesnel/postgres_exporter   
(go run mage.go查看所有可以使用的)  
go run mage.go binary


[root@bogon src]# vim postgresql_exports_test.sh 
export   DATA_SOURCE_NAME=postgresql://postgres:postgres@172.16.0.159:5432/postgres?sslmode=disable  
nohup /root/go/src/github.com/wrouesnel/postgres_exporter/postgres_exporter --web.listen-address=":9180" &>/tmp/postgres1.log &

无法监控存储情况，对于云服务器的rds不适用