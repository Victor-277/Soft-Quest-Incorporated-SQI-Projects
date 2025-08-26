from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    countries =[
            ("Nigeria", "Nigeria"),
            ("Ghana", "Ghana"),
            ("United kindow", "UK"),
            ("USA", "USA"),


    ]

    states =[
        ("Abia", "Abia"),
        ("Oyo", "Oyo"),
        ("Osun", "Osun"),
        ("Lagos", "Lagos"),
        ("Kano", "Kano"),
        ("Abuja", "Abuja"),
    ]

    position = [
        ("MD", "MD"),
        ("CEO", "CEO"),
        ("HOD", "HOD"),
        ("Secretary", "Secretary"),
        ("Accountant", "Accountant"),
        ("Admin", "Admin"),
        ("Customer care", "Customer care"),
    

    ]

    dept = [
        ("Customer care", "Customer care"),
        ("Accountant", "Accountant"),
        ("HR", "HR"),
        ("Marketing", "Marketing"),
        
        
    ]

    ma_status = [
            ("Single", "Single"),
            ("Married", "Married"),
            ("Divorce", "Divorce"),
            ("Complicate", "Complicate"),
    ]


    staff_status = [
            ("Active", "Active"),
            ("Suspended", "Suspended"),
            ("On level", "On level"),
            ("Resigned", "Resigned"),
            ("Retired", "Retired"),

    ]
    

    identity_name = [
            ("internation passport", "internation passport"),
            ("Driver's licence", "Driver's licence"),
            ("Voter's card", "Voter's card"),
            ("NIMC", "NIMC"),
    ]
    

    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    address = models.CharField(unique=False, max_length=100, null=True)
    phone = models.CharField(unique=True, max_length=11, null=True)
    email = models.EmailField(unique=True, max_length=11, null=True, default=None)
    date_of_birth = models.DateField(unique=False, max_length=11, null=True)
    gender = models.CharField(unique=False, max_length=11, null=True)
    nationality = models.CharField(choices=countries, unique=False, max_length=50, null=True)
    state = models.CharField(choices=states, unique=False, max_length=20, null=True)
    mean_of_identity = models.ImageField(upload_to='identityImage/', unique=False, null=True)
    particulars = models.FileField(upload_to='particularsImage/', unique=False, null=True)
    profile_passport = models.ImageField (upload_to='staffImage/', unique=False, null=True)
    profile_picture = models.ImageField (upload_to='profileImage/', unique=False, null=True)
    position = models.CharField(choices=position, unique=False, max_length=25, null=True)
    department = models.CharField(choices=dept, unique=False, max_length=25, null=True)
    marital_status = models.CharField(choices=ma_status, unique=False, max_length=25, null=True)
    staff = models.BooleanField(default=False, unique=False)
    nex_of_kin  = models.CharField (unique=False, max_length=20, null=True)
    status = models.CharField(choices=staff_status, unique=False, max_length=10, null=True, default="Active")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()       