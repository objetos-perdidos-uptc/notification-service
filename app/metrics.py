from prometheus_client import Counter

EMAILS_SENT = Counter('notification_emails_sent_total', 'Total de correos enviados exitosamente')
EMAILS_FAILED = Counter('notification_emails_failed_total', 'Total de correos fallidos')
