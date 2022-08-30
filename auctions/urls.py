from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/newcomment", views.newcomment, name="newcomment"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.opencategory, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/watchlist", views.watch, name="watch"),
    path("<int:listing_id>/removewatch", views.notwatch, name="notwatch")
]
