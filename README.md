# Zimbra Dashboard

Zimbra Prometheus Exporter + Grafana Dashboard

The following environment is required and tested:
* Zimbra 8.8.15 
* Python 3.6
* Prometheus 2.18
* Grafana 8.2.5



```bash
pip3 install flask
pip3 install prometheus_client
pip3 install psutil

wget https://raw.githubusercontent.com/jasoncheng7115/zimbra_dashboards/main/zimbra_exporter.py -O /opt/zimbra_exporter.py
chmod +x /opt/zimbra_exporter.py

wget https://raw.githubusercontent.com/jmutai/telegraf-ansible/master/templates/zimbra_pflogsumm.pl.j2 -O /opt/zimbra_pflogsumm.pl
chmod +x /opt/zimbra_pflogsumm.pl

wget https://raw.githubusercontent.com/jasoncheng7115/zimbra_dashboards/main/zimbra_exporter.service -O /etc/systemd/system/zimbra_exporter.service

systemctl daemon-reload
systemctl start zimbra_exporter
systemctl enable zimbra_exporter

```


>  p.s:The zimbra part of the stats information uses jmutai's "zimbra_pflogsumm.pl" to handle log data
