from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class EventDates(models.Model):
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    type = models.CharField(max_length=100,default="home");
    name = models.CharField(default="",max_length=100)

    def __str__(self) -> str:
        return self.name + ' starts at : '+self.event_start.isoformat() + ' ends at : '+self.event_end.isoformat()

class Merch(models.Model):
    SIZES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )
    COLORS = (
        ('Black','Black'),
        ('White','White')
    )
    BOOL = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    PAYMENT = (
        ('Kshitiz', 'Kshitiz'),
        ('Adarsh', 'Adarsh')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    from_college = models.CharField(choices=BOOL, max_length=5,)
    reg_no = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=10)
    hall_no = models.CharField(max_length=5)
    room_no = models.CharField(max_length=5)
    address = models.CharField(max_length=50)
    size = models.CharField(choices=SIZES, max_length=5)
    payment = models.CharField(choices=PAYMENT,max_length=50, blank=True)
    verified = models.BooleanField()

    def __str__(self):
        return self.name + " | " + self.phone_number

class Proof(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField( upload_to="images/", blank=False)

    def __str__(self):
        return self.user.email + " | Payment proof" 
    
class Pass(models.Model):
    PLAN_CHOICES = [
        ('gold', 'Gold 300/-'),
        ('platinum', 'Platinum 600/-'),
        ('vip', 'VIP 900/-'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    verified = models.BooleanField(default=False)
    image = models.FileField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.plan}"


