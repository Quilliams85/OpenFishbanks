from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("<int:id>", views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('buy_ship/<int:ship_id>/', views.buy_ship, name='buy_ship'),
    path('myprofile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]