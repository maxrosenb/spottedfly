from django.contrib import admin
from .models import Playlist, Comment, Profile

admin.site.register(Playlist)
admin.site.register(Comment)
admin.site.register(Profile)