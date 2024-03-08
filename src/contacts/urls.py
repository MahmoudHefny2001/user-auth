from django.urls import path, include


from . import views

urlpatterns = [

    path("send/", views.SendForm.as_view(), name="send_form"),
]