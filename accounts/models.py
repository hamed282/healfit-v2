from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.core.exceptions import ValidationError


class RoleModel(models.Model):
    role = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.role}'


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    trn_number = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=22, null=True, blank=True)
    zoho_customer_id = models.CharField(max_length=128, null=True, blank=True)
    password = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class RoleUserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE)


class AddressModel(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
    address = models.TextField()
    additional_information = models.TextField(null=True, blank=True)
    emirats = models.CharField(max_length=100, null=True, blank=True)
    prefix_number = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    iban_country = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.user}'


class CurrentAddressModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        if self.address.user != self.user:
            raise ValidationError("The address does not belong to the user.")
        super(CurrentAddressModel, self).save(*args, **kwargs)
