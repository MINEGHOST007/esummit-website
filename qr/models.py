from django.db import models
from django.contrib.auth.models import User
import json, uuid

MAX_TIER = 5

def initial(n):
    triangular_array = []
    for i in range(n):
        row = [0] * (i + 1)
        triangular_array.append(row)
    return triangular_array

def initial_json():
    return json.dumps(initial(MAX_TIER))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.TextField(default='https://ui-avatars.com/api/?name=John+Sha&background=fdba74&color=282319')
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=50)
    registration = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    collections = models.JSONField(default=initial_json)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ' | ' + str(self.mobile)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Card(models.Model):
    name = models.CharField(max_length=25)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    tier = models.IntegerField()
    identity = models.IntegerField()
    point = models.IntegerField()

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        unique_together = ['tier', 'identity']

    def __str__(self):
        return self.name + ' | ' + str(self.tier) + ' | ' + str(self.identity)

class Qr(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    uniqueId = models.CharField(primary_key=True, default='', editable=False, unique=True, max_length=12)
    
    def generate_unique_id(self):
        return uuid.uuid4().hex[:12].upper()

    def save(self, *args, **kwargs):
        if not self.uniqueId:
            self.uniqueId = self.generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.card) + ' | ' + str(self.uniqueId)

class Scan(models.Model):
    qr = models.ForeignKey(Qr, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['qr', 'profile']
        verbose_name = 'Scan'
        verbose_name_plural = 'Scans'

    def __str__(self):
        return str(self.qr) + ' scanned by ' + self.profile.name
