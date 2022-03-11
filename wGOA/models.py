from django.db import connections
from django.db import models

# from datetime import datetime
# import pytz
# local_tz = pytz.timezone("Asia/Singapore")
# utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
# local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))

class cpc(models.Model):
    Time = models.CharField(max_length=100)
    N = models.CharField(max_length=15)
    class Meta:
        db_table = "cpc_ubi"

class cpc2(models.Model):
    ID = models.CharField(max_length = 100)
    N = models.CharField(max_length = 15)
    class Meta:
        db_table = "cpc_ubi_1"

class neph2(models.Model):
    ID = models.CharField(max_length= 15 )
    sblue = models.CharField(max_length = 15)
    sred = models.CharField(max_length = 15)
    sgreen = models.CharField(max_length = 15)
    bsblue = models.CharField(max_length = 15)
    bsred = models.CharField(max_length = 15)
    bsgreen = models.CharField(max_length = 15)
    class Meta:
        db_table = "neph_ubi_1"



class instrument(models.Model):

    name = models.CharField(max_length=100)
    desc = models.TextField()
    img = models.ImageField(upload_to='pics')