from django.contrib import admin
from .models import User, Show, Review, Rating

admin.site.register(User)
admin.site.register(Show)
admin.site.register(Review)
admin.site.register(Rating)