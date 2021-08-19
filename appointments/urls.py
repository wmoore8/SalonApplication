from django.urls import path

from .views import (
    appointment_list_view,
    appointment_delete_view,
    appointment_create_view,
    appointment_detail_view,
)

app_name = 'appointments'
urlpatterns = [
    path('', appointment_list_view, name='appointments'),
    path('create/', appointment_create_view, name='appointment-create'),
    path('<int:id>/detail/delete/', appointment_delete_view, name='appointment-delete'),
    path('<int:id>/detail/', appointment_detail_view, name='appointment-detail'),

]
