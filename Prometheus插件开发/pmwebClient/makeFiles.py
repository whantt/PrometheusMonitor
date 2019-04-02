# coding: utf-8
import json

nameClient = 'prometheus_client'
job_path = '/tmp/federal/'   # 必须以/结尾
ping_flag = True
prometheus_path = '/tmp/federal/'  # 必须以/结尾

modelConfig = """
## {{ name }}

global:
  scrape_interval: 60s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 60s # Evaluate rules every 15 seconds. The default is every 1 minute.
  scrape_timeout: 20s # 设定抓取数据的超时时间，默认为10s

alerting:
  alertmanagers:
  - static_configs:
    - targets:

rule_files:

scrape_configs:
  {{ scrape_configs }}

"""

jobConfig = """
  - job_name: '{{ name }}'
    scrape_interval: {{ scrape_interval }}
    honor_labels: true
    metrics_path: '{{ metrics_path }}'
    {{ params }}
    {{ type }}
    file_sd_configs:
    - files:
      - {{ file }}
"""

pingConfig = """
  - job_name: 'check-ping'
    scrape_interval: 30s
    metrics_path: '/probe'
    params:
      module: [icmp]

    file_sd_configs:
    - files:
      - {{ path }}

    relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: 127.0.0.1:9115
"""


def makeConfig(data):
    # global job_path
    try:

        _config = modelConfig
        _config = _config.replace('{{ name }}', nameClient)
        # _config = _config.replace('{{ scrape_interval }}', scrape_interval)
        # _config = _config.replace('{{ evaluation_interval }}', evaluation_interval)
        # _config = _config.replace('{{ scrape_timeout }}', scrape_timeout)
        # _config = _config.replace('{{ url }}', alertmanagers_targets)

        # 加载组信息
        # gp = Group.objects.filter(federalid='')
        # _group = []
        rule_path = ""
        jobs = ""
        # for index in range(0, len(gp)):
        for key in data.keys():
            if key == 'type':
                continue
            # scrape_interval = data[key]['scrape_interval']
            # metrics_path = data[key]['metrics_path']
            # scheme = data[key]['scheme']
            # insecure_skip_verify = data[key]['insecure_skip_verify']
            # match = data[key]['match']

            # 修改job配置
            if "" == jobs:
                jobs = jobConfig.replace('{{ name }}', key)
                jobs = jobs.replace('{{ scrape_interval }}', data[key]['scrape_interval'])

                if "" != data[key]['metrics_path']:
                    jobs = jobs.replace('{{ metrics_path }}', data[key]['metrics_path'])
                else:
                    jobs = jobs.replace('{{ metrics_path }}', '/metrics')

                if "" != data[key]['scheme'] and "https" == data[key]['scheme']:
                    httpsmode = 'scheme: https'
                    httpsmode = httpsmode + '\n    tls_config:'
                    httpsmode = httpsmode + '\n      insecure_skip_verify: ' + data[key]['insecure_skip_verify']
                else:
                    httpsmode = 'scheme: http'

                jobs = jobs.replace('{{ type }}', httpsmode)

                if "" != data[key]['match'].strip():
                    match = 'params:'
                    match = match + '\n      match[]:'
                    for mc in data[key]['match'].strip().split(','):
                        if "" != mc:
                            match = match + "\n      - '" + mc + "'"

                    jobs = jobs.replace('{{ params }}', match)
                else:
                    jobs = jobs.replace('{{ params }}', '')

                _file = job_path + key + '.yml'
                jobs = jobs.replace('{{ file }}', _file)
            else:
                jobEx = jobConfig.replace('{{ name }}', key)
                jobEx = jobEx.replace('{{ scrape_interval }}', '30s')

                if "" != data[key]['metrics_path']:
                    jobEx = jobEx.replace('{{ metrics_path }}', data[key]['metrics_path'])
                else:
                    jobEx = jobEx.replace('{{ metrics_path }}', '/metrics')

                if "" != data[key]['scheme'] and "https" == data[key]['scheme']:
                    httpsmode = 'scheme: https'
                    httpsmode = httpsmode + '\n    tls_config:'
                    httpsmode = httpsmode + '\n      insecure_skip_verify: ' + data[key]['insecure_skip_verify']
                else:
                    httpsmode = 'scheme: http'

                jobEx = jobEx.replace('{{ type }}', httpsmode)

                if "" != data[key]['match'].strip():
                    match = 'params:'
                    match = match + '\n      match[]:'
                    for mc in data[key]['match'].strip().split(','):
                        if "" != mc:
                            match = match + "\n      - '" + mc + "'"

                    jobEx = jobEx.replace('{{ params }}', match)
                jobEx = jobEx.replace('{{ params }}', '')
                _file = job_path + key + '.yml'
                jobEx = jobEx.replace('{{ file }}', _file)

                jobs = jobs + '\n' + jobEx

        _config = _config.replace('{{ scrape_configs }}', jobs)

        _config = _config.replace('{{ rule_files }}', rule_path)
        _c = ''
        if ping_flag is True:
            _c = makePingConfig()

        _config += '\n' + _c + '\n'
    except Exception, e:
        print e, u'配置文件信息替换错误'
        return modelConfig
    return _config


def makePingConfig():

    filepath = job_path + 'check-ping.yml'
    # _config = pingConfig.replace('{{ job_name }}', name)
    # _config = _config.replace('{{ interval }}', interval)
    # _config = _config.replace('{{ uri }}', uri)
    # _config = _config.replace('{{ url }}', url)
    _config = pingConfig.replace('{{ path }}', filepath)

    return _config


def writePrometheusConfig(content):
    with open(prometheus_path + 'prometheus.yml', 'w') as f:
        f.write(content)


def writePrometheusJobFile(data):
    for key in data.keys():
        if key == 'type':
            continue

        with open(prometheus_path + key + '.yml', 'w') as f:
            f.write(json.dumps(data[key]['value'], ensure_ascii=False))


def writePrometheusPingFile(data):
    with open(prometheus_path + 'remote-ping.yml', 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False))
