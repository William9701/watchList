from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),  
    path("new_show", views.new_show, name="new_show"),
    path("show/<int:show_id>", views.show_view, name="show_view"),
    path("show/<int:show_id>/rate", views.rate_show, name="rate_show"),
    path("favorites", views.index,{'showpage': 'favorites'}, name="favorites"),
    path("recommendations", views.index,{'showpage': 'recommendations'}, name="recommendations"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("search", views.index, {'showpage': 'search_results'}, name="search"),

    # API routes
    path("edit_show", views.edit_show, name="edit_show"),
    # path("like_post", views.like_post, name="like_post"),
]