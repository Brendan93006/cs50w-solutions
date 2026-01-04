from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>/", views.listing_view, name="listing"),
    path("categories", views.categories_view, name="categories"),
    path("category/<str:category>/", views.category_listings, name="category"),
    path("watchlist/", views.watchlist_listings, name="watchlist"),
    path("listing/<int:listing_id>/closed/", views.closed_listing, name="closed_listing")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
