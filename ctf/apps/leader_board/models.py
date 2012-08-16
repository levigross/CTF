from django.db import models
from datetime import datetime
from hashlib import sha512

CHALLENGE_TYPES = (
    ('RE', 'Reversing'),
    ('WE', 'Web Exploitation'),
    ('AE', 'Application Exploitation'),
    ('CR', 'Crypto'),
    )

class UserHandle(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    handle_name = models.CharField(max_length=100, unique=True)
    time_finished = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.updated_on = datetime.utcnow()

        if self.score >= 100:
            self.time_finished = datetime.utcnow()

        super(UserHandle, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.handle_name

    @property
    def precent_score(self):
        return 0 if not self.score else int((float(self.score) / 2000.0) * 100.0)


class Challenge(models.Model):
    challenge_type = models.CharField(max_length=2, choices=CHALLENGE_TYPES)
    points = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    guide = models.TextField()
    hint = models.TextField()

    def __unicode__(self):
        return u"{0} - {1}".format(self.title, self.get_challenge_type_display())


class Flag(models.Model):
    challenge_type = models.ForeignKey(Challenge, related_name='challenge_types')
    success_flag = models.CharField(max_length=1000, unique=True)

    def save(self, *args, **kwargs):
        if len(self.success_flag) != 128:
            self.success_flag = sha512(self.success_flag.strip()).hexdigest()
        super(Flag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.challenge_type.title


class CompletedChallanges(models.Model):
    user_handle = models.ForeignKey(UserHandle, unique=True, related_name="completed_challanges")
    challange = models.ManyToManyField(Challenge, related_name="completed_challanges")

    def __unicode__(self):
        return u"{0} - {1}".format(self.user_handle, self.challange.count())
