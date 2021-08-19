from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Appointment
from .forms import AppointmentForm, CommentForm
from accounts.views import get_name
from django.contrib.auth.decorators import login_required

@login_required
def appointment_list_view(request, *args, **kwargs):
    appointment_queryset = Appointment.objects.all()

    username = get_name(request)

    my_context = {
        "appointment_list": appointment_queryset,
        "appointment_form": AppointmentForm,
        'username': username
    }

    return render(request, "appointment_list.html", my_context)

@login_required
def appointment_delete_view(request, id):
    obj = get_object_or_404(Appointment, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect(reverse("appointments:appointments"))

    context = {
        "obj": obj
    }
    return render(request, "appointments_delete.html", context)

@login_required
def appointment_create_view(request):
    username = request.user.get_full_name()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appt = Appointment()
            appt.customer = username
            appt.service = form.cleaned_data['service']
            appt.stylist = form.cleaned_data['stylist']
            appt.start_date = form.cleaned_data['start_date']
            appt.start_time = form.cleaned_data['start_time']

            appt.save()
            return redirect('../')

    else:
        initial = {'customer': username}
        form = AppointmentForm(initial=initial)

    return render(request, 'appointments_create.html', {'form': form})

@login_required
def appointment_detail_view(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    username = get_name(request)
    # List of active comments for this post
    comments = appointment.appointment_comments

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment, add author's name
            new_comment.author = request.user.get_full_name()
            new_comment.appointment = appointment
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'appointment_detail.html',
                  {'appointment': appointment,
                   'username': username,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})