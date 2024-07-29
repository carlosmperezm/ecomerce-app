from typing import override

from django.db.models import Model,EmailField,CharField,ForeignKey,SET_NULL
from django.contrib.auth.models import AbstractUser,BaseUserManager


class Address(Model):
    street:CharField = CharField(max_length=100)
    city:CharField = CharField(max_length=100)
    state:CharField = CharField(max_length=100)
    zip_code:CharField = CharField(max_length=10)
    number:CharField = CharField(max_length=100)

    @override
    def __str__(self) -> str:
        return f'{self.street},{self.city},{self.state},{self.zip_code}'

class User(AbstractUser):
    email:EmailField = EmailField(verbose_name='email address',unique=True,max_length=100)
    username:CharField = CharField(max_length=100,unique=True)
    phone_number:CharField = CharField(max_length=15,null=True,blank=True)
    address:ForeignKey = ForeignKey(Address,on_delete=SET_NULL,null=True,blank=True)

    REQUIRED_FIELDS = ['email']

    @override
    def __str__(self) -> str:
        return str(self.email)
    

