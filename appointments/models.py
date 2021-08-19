from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
import datetime


class Service(models.Model):
    title = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    duration = models.IntegerField(default=60)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Stylist(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def booked_appointments(self):
        return Appointment.objects.filter(stylist_id=self.pk)

    def get_availability_for_date(self, date):
        availability = [
            ('10:00 AM', '10:00 AM'),
            ('11:00 AM', '11:00 AM'),
            ('12:00 PM', '12:00 PM'),
            ('1:00 PM', '1:00 PM'),
            ('2:00 PM', '2:00 PM'),
            ('3:00 PM', '3:00 PM'),
            ('4:00 PM', '4:00 PM'),
            ('5:00 PM', '5:00 PM'),
            ('6:00 PM', '6:00 PM'),
        ]

        appointments_on_date = Appointment.objects.filter(stylist_id=self.pk, start_date=date)
        print(appointments_on_date)
        for appointment in appointments_on_date:
            for time in availability:
                if time[0] == appointment.start_time:
                    availability.remove(time)

        return availability

    class Meta:
        ordering = ['name']


class Appointment(models.Model):
    availability = [
        ('10:00 AM', '10:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('12:00 PM', '12:00 PM'),
        ('1:00 PM', '1:00 PM'),
        ('2:00 PM', '2:00 PM'),
        ('3:00 PM', '3:00 PM'),
        ('4:00 PM', '4:00 PM'),
        ('5:00 PM', '5:00 PM'),
        ('6:00 PM', '6:00 PM'),
    ]

    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    stylist = models.ForeignKey(Stylist, on_delete=models.DO_NOTHING)
    customer = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.CharField(max_length=10, null=True, choices=availability)
    is_booked = models.BooleanField(default=False)

    def appointment_comments(self):
        return Comment.objects.filter(appointment__pk=self.pk)

    def get_appointments(self):
        return Appointment.objects.all()

    def get_absolute_url(self):
        return reverse("appointments:appointment-detail", kwargs={"id": self.id})

    def __str__(self):
        return self.service.title + ' with ' + self.stylist.name + ' at ' + self.start_time.__str__()

    class Meta:
        ordering = ['start_date']

    def clean(self):
        if self.start_date <= datetime.date.today():
            raise ValidationError('Please choose a future appointment date.')

        if self.start_date.weekday() == 6 or self.start_date.weekday() == 0:
            raise ValidationError('Salon is closed on Sunday and Monday. Please choose a day Tuesday-Saturday')

        appointments_for_stylist = self.stylist.booked_appointments()
        for appointment in appointments_for_stylist:
            if self.start_date == appointment.start_date:
                if self.start_time == appointment.start_time:
                    raise ValidationError('Stylist already booked at chosen date and time, please choose another time')


class AppointmentTime(models.Model):
    test_start_time = models.CharField(max_length=10, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField(null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)

    class Meta:
        ordering = ['created_date']
