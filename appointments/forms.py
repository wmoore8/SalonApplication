from django import forms
from django.urls import reverse
from .models import Appointment, Comment, AppointmentTime, Stylist


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'service',
            'stylist',
            'start_date',
            'start_time',
        ]

        widgets = {
            'start_date': DateInput(),
        }

    def get_absolute_url(self):
        return reverse("appointments:appointment-create")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def get_absolute_url(self):
        return reverse("appointments:comment-create")
