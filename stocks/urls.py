from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('membersonly/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('', include('quotes.urls')),

]
