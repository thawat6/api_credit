from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group
from rolepermissions.roles import assign_role, remove_role


ROLE_CHOICES = (
    ('driver', 'driver'),
    ('admin', 'Admin'),
    ('judge', 'Judge'),
    ('teacher', 'Teacher'),
    ('student', 'Student')
)


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        remove_role(self.user, self.role)
        assign_role(self.user, self.role)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
