from django.db import models
from django.contrib.auth.models import User
import hashlib


class Ribbit(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email.encode('utf-8')).hexdigest()


'''
This line create a user if it is not present and sets the profile attribute (which is created dynamically) of User class
to it.
So, whenever user.profile is called it will come to this line and return or create and return a user
'''
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
