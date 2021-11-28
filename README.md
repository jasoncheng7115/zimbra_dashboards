# Zimbra Dashboard

Zimbra + Prometheus Exporter + Grafana Dashboard

base on Python 3.6+

```
pip3 install flask
pip3 install prometheus_client
pip3 install psutil

wget https://raw.githubusercontent.com/jmutai/telegraf-ansible/master/templates/zimbra_pflogsumm.pl.j2 -O /opt/zimbra_pflogsumm.pl
chmod +x /opt/zimbra_pflogsumm.pl

wget https://raw.githubusercontent.com/jasoncheng7115/zimbra_dashboards/main/zimbra_exporter.service -O /etc/systemd/system/zimbra_exporter.service
systemctl daemon-reload
systemctl start zimbra_exporter
systemctl enable zimbra_exporter

```

