from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()

alerts_needing_update = Alert.find_needing_updates()

for alert in alerts_needing_update:
    alert.load_item()
    alert.send_mail_if_price_reached()
