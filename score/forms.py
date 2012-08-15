from hashlib import sha512
from time import sleep
from random import randint

from django.utils.crypto import constant_time_compare
from django import forms
from models import UserHandle, Flag

class HandleSubmissionForm(forms.ModelForm):

    class Meta:
        model = UserHandle
        fields = ('handle_name',)

class FlagSubmitForm(forms.ModelForm):
    class Meta:
        model = Flag


    def clean_success_flag(self):
        flag = self.cleaned_data.get('success_flag')
        if not flag:
            raise forms.ValidationError("You have no submitted a flag")

        flag = sha512(flag.strip()).hexdigest()
        sleep(randint(1,5))
        if not Flag.objects.filter(success_flag=flag).exists():
            raise forms.ValidationError("This flag does not exist within the Database!")
        
        db_flag = Flag.objects.get(success_flag=flag)

        if not constant_time_compare(db_flag.success_flag, flag):
            raise forms.ValidationError("This flag does not exist within the Database!")

        return db_flag.challenge_type_id
