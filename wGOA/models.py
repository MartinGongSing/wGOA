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
    ID = models.CharField(max_length= 100)
    sblue = models.CharField(max_length = 15)
    sred = models.CharField(max_length = 15)
    sgreen = models.CharField(max_length = 15)
    bsblue = models.CharField(max_length = 15)
    bsred = models.CharField(max_length = 15)
    bsgreen = models.CharField(max_length = 15)
    class Meta:
        db_table = "neph_ubi_1"

class psap(models.Model):
    ID = models.CharField(max_length= 100)
    blue = models.CharField(max_length = 15)
    red = models.CharField(max_length = 15)
    green = models.CharField(max_length = 15)

    class Meta:
        db_table = "psap_ubi"

class aps(models.Model):
    ID = models.CharField(max_length= 100)
    d1 = models.CharField(max_length=15)
    d2 = models.CharField(max_length=15)
    d3 = models.CharField(max_length=15)
    d4 = models.CharField(max_length=15)
    d5 = models.CharField(max_length=15)
    d6 = models.CharField(max_length=15)
    d7 = models.CharField(max_length=15)
    d8 = models.CharField(max_length=15)
    d9 = models.CharField(max_length=15)
    d10 = models.CharField(max_length=15)
    d11 = models.CharField(max_length=15)
    d12 = models.CharField(max_length=15)
    d13 = models.CharField(max_length=15)
    d14 = models.CharField(max_length=15)
    d15 = models.CharField(max_length=15)
    d16 = models.CharField(max_length=15)
    d17 = models.CharField(max_length=15)
    d18 = models.CharField(max_length=15)
    d19 = models.CharField(max_length=15)
    d20 = models.CharField(max_length=15)
    d21 = models.CharField(max_length=15)
    d22 = models.CharField(max_length=15)
    d23 = models.CharField(max_length=15)
    d24 = models.CharField(max_length=15)
    d25 = models.CharField(max_length=15)
    d26 = models.CharField(max_length=15)
    d27 = models.CharField(max_length=15)
    d28 = models.CharField(max_length=15)
    d29 = models.CharField(max_length=15)
    d30 = models.CharField(max_length=15)
    d31 = models.CharField(max_length=15)
    d32 = models.CharField(max_length=15)
    d33 = models.CharField(max_length=15)
    d34 = models.CharField(max_length=15)
    d35 = models.CharField(max_length=15)
    d36 = models.CharField(max_length=15)
    d37 = models.CharField(max_length=15)
    d38 = models.CharField(max_length=15)
    d39 = models.CharField(max_length=15)
    d40 = models.CharField(max_length=15)
    d41 = models.CharField(max_length=15)
    d42 = models.CharField(max_length=15)
    d43 = models.CharField(max_length=15)
    d44 = models.CharField(max_length=15)
    d45 = models.CharField(max_length=15)
    d46 = models.CharField(max_length=15)
    d47 = models.CharField(max_length=15)
    d48 = models.CharField(max_length=15)
    d49 = models.CharField(max_length=15)
    d50 = models.CharField(max_length=15)
    d51 = models.CharField(max_length=15)
    d52 = models.CharField(max_length=15)

    class Meta:
        db_table = "aps_ubi"





class instrument(models.Model):

    name = models.CharField(max_length=100)
    desc = models.TextField()
    img = models.ImageField(upload_to='pics')


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email