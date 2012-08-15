import datetime

from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from forms import HandleSubmissionForm, FlagSubmitForm
from models import UserHandle, Challenge, CompletedChallanges


class Home(TemplateView):
    template_name = "score/home.html"

    def post(self, request, *args, **kwargs):
        if 'user_handle' in self.request.session:
            return redirect('leader_board')

        if not request.session.test_cookie_worked():
            messages.add_message(self.request, messages.INFO,
                "You must enable cookies in order for this application to work")
            return self.get(request)

        request.session.delete_test_cookie()

        handle_form = HandleSubmissionForm(self.request.POST)
        if handle_form.is_valid() and handle_form.save(commit=False):
            handle_form.save()
            handle_name = handle_form.cleaned_data.get('handle_name')
            messages.add_message(self.request, messages.INFO, u"Welcome to HackNight! {0}".format(handle_name))
            self.request.session['user_handle'] = handle_name
            return redirect('leader_board')
        else:
            return self.get(request, form=handle_form)


    def get_context_data(self, **kwargs):
        self.request.session.set_test_cookie()
        return {
            'form': kwargs['form'] if 'form' in kwargs else HandleSubmissionForm()
        }


class LeaderBoard(TemplateView):
    template_name = 'score/leaderboard.html'

    def get_context_data(self, **kwargs):
        return {
            'all_users': tuple(UserHandle.objects.all().order_by('-score', 'updated_on')),
            }


class Flag(TemplateView):
    template_name = 'score/flag.html'

    def post(self, request):
        flag_form = FlagSubmitForm(self.request.POST)
        if flag_form.is_valid():
            user_handle = get_object_or_404(UserHandle, handle_name=self.request.session.get("user_handle"))
            completed = Challenge.objects.get(id=flag_form.cleaned_data.get('success_flag'))
            com = CompletedChallanges.objects.get_or_create(user_handle=user_handle)[0]

            if completed in com.challange.all():
                messages.add_message(self.request, messages.INFO,
                    "You cannot complete a challenge twice!".format(completed))
                return self.get(self.request)

            com.challange.add(completed)
            com.save()
            user_handle.score += completed.points
            user_handle.save()

            messages.add_message(self.request, messages.INFO,
                u"Congratulations on completing challenge {0}!".format(completed))
            self.request.session.cycle_key()
            self.request.session['user_handle'] = user_handle.handle_name
            return redirect('leader_board')
        else:
            return self.get(request, form=flag_form)

    def get(self, request, *args, **kwargs):
        if 'user_handle' not in self.request.session:
            messages.add_message(self.request, messages.INFO,
                "You must have a User Handle to submit a flag")
            return redirect('leader_board')
        else:
            return super(Flag, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            "form": kwargs['form'] if 'form' in kwargs else FlagSubmitForm()
        }


class Challenges(TemplateView):
    template_name = 'score/challenges.html'

    def get_context_data(self, **kwargs):
        return {
            'challanges': tuple(Challenge.objects.all().order_by('points')),
            }
