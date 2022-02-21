from django.db import connections
from django.db import models

# from datetime import datetime
# import pytz
# local_tz = pytz.timezone("Asia/Singapore")
# utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
# local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))

class CPC(models.Model):
    cpctime = models.CharField(max_length=100)
    N = models.CharField(max_length=15)
    class Meta:
        db_table = "CPC_UBI"