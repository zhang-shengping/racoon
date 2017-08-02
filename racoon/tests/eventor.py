from oslo_config import cfg
import oslo_messaging

CONF = cfg.CONF
CONF(default_config_files=["/etc/ceilometer/ceilometer.conf"])

url = 'rabbit://openstack:RABBIT_PASS@172.18.211.4/'
transport = oslo_messaging.get_notification_transport(
    CONF, url, allowed_remote_exmods=None)

notifier = oslo_messaging.Notifier(transport,
    driver='messagingv2', topics=['test2'])

notifier.info({},'test',{})

print notifier
