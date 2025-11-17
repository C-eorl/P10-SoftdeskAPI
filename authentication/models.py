from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_age(date_of_birth):
    """ Validate user's age +15"""
    if date_of_birth:
        today = date.today()
        age = today.year - date_of_birth.year - (
                (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        if age < 15:
            raise ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")

class CustomUser(AbstractUser):
    """User with RGPD conformity"""
    date_of_birth = models.DateField(validators=[validate_age], null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            return age
        return None