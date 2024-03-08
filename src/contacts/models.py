from django.db import models

from django_extensions.db.models import TimeStampedModel

from users.validators import valid_phone_number


class ContactForm(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12, validators=[valid_phone_number])
    message = models.TextField()
    
    def __str__(self):
        return self.name
    

    class Meta:
        db_table = "contact_form"
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Forms"
        ordering = ["-created"]