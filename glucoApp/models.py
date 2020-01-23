from datetime import datetime

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


def get_obs_upload_path(instance, filename):
    today = datetime.now()
    if today.hour < 12:
        h = "00"
    else:
        h = "12"
    return '%s/%s' % (today.strftime('%Y%m%d')+ h, filename)
# Create your models here.
class Experiment(models.Model):
    image=models.ImageField("Image",null=True,blank=True,upload_to=get_obs_upload_path)
    value=models.CharField("Value",null=True,blank=True,max_length=10)
    is_confirmed=models.BooleanField("Confirm",default=False)
    date_added=models.DateTimeField(auto_now_add=True)



    def to_json(self):
        return {
            'id': self.id,
            'value': self.value,
            'is_confirmed': self.is_confirmed,
            'date_added': self.date_added

        }

@receiver(post_delete, sender=Experiment)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
