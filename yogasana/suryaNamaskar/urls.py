from django.contrib import admin
from django.urls import path, include
from suryaNamaskar import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('start', views.start),
    path('suryanamaskar', views.suryanamaskar),
    path('Home', views.Home),
    #path('suryaFrame', views.suryaFrame)
    # path('suryanamaskar', views.suryanamaskar, name=='suryanamaskar')
]