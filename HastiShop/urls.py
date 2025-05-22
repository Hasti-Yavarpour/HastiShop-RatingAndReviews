from django.contrib import admin
from django.urls import path, include
from shop import views  # ✅ import your app's views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('', views.home_view, name='home'),  # ✅ Home page
]

