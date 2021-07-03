from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)
DEPT_CHOICES = (
    ("IT", "TT"),
    ("Account", "Account"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dept = models.CharField(max_length=20, choices=DEPT_CHOICES)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
    # if created:
    #     Profile.objects.create(user=instance)
    # instance.profile.save()


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)

    def __str__(self):
        return self.product_name


class Indent(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.FloatField(blank=True)
    product_quantity = models.IntegerField(null=True)
    requested_amount = models.FloatField(null=False, blank=True, default=0)
    paid_amount = models.FloatField(null=True, default=0)
    balance = models.FloatField(null=True, default=0)

    def save(self, *args, **kwargs):
        self.requested_amount = self.product_price * self.product_quantity
        self.balance = self.requested_amount - self.paid_amount
        super(Indent, self).save(*args, **kwargs)

    def __str__(self):
        return self.category
