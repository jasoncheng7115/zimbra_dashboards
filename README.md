# Zimbra Dashboard

Zimbra Prometheus Exporter + Grafana Dashboard

* Grafana dashboard:
  https://grafana.com/orgs/jason5961


![Demo](https://github.com/jasoncheng7115/zimbra_dashboards/blob/main/dashboard_english.png?raw=true)


The following environment is tested:
* Ubuntu 18.04
* Zimbra 8.8.15 
* Python 3.6
* Prometheus 2.18
* Grafana 8.2.5


---



  

```
pip3 install flask
pip3 install prometheus_client
pip3 install psutil

wget https://raw.githubusercontent.com/jasoncheng7115/zimbra_dashboards/main/zimbra_exporter.py -O /opt/zimbra_exporter.py
chmod +x /opt/zimbra_exporter.py

wget https://raw.githubusercontent.com/jmutai/telegraf-ansible/master/templates/zimbra_pflogsumm.pl.j2 -O /opt/zimbra_pflogsumm.pl
chmod +x /opt/zimbra_pflogsumm.pl
```

>  p.s: the zimbra part of the stats information uses jmutai's "zimbra_pflogsumm.pl" to get log statistics.

  
    
Required Modified variables in the zimbra_exporter.py:

```
PORT_EXPORTER = 9093

MAILSERVER = 'mail.zimbra.domain'
EXCLUDE_DOMAIN = '' # If you want to filter out a specific domain, please add it here.

PORT_SMTP = '25'
PORT_IMAP = '143'
PORT_IMAPS = '993'
PORT_POP3 = '110'
PORT_POP3S = '995'
PORT_WEBCLIENT = '443'
```
  
  
## Add prometheus scrape config:
```
 # Zimbra Exporter
  - job_name: 'zimbra'
    scrape_interval: 60s
    scrape_timeout: 30s
    honor_labels: true
    static_configs:
    - targets: ['zimbraserver:9093']
```


## Set to run as a service:

```
wget https://raw.githubusercontent.com/jasoncheng7115/zimbra_dashboards/main/zimbra_exporter.service -O /etc/systemd/system/zimbra_exporter.service

systemctl daemon-reload
systemctl start zimbra_exporter
systemctl enable zimbra_exporter
```
