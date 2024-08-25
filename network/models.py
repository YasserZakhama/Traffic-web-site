from django.db import models

class Packet(models.Model):
    timestamp = models.DateTimeField()
    source_ip = models.CharField(max_length=15)
    destination_ip = models.CharField(max_length=15)
    protocol = models.CharField(max_length=10)
    length = models.IntegerField()
    info = models.TextField()

    def __str__(self):
        return self.source_ip

