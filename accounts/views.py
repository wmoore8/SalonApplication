from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic


class AppointmentUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)


# Create your views here.
class SignUpView(generic.CreateView):
    form_class = AppointmentUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def get_name(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        return username
