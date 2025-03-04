from django.urls import path
from . import views
from .views import get_game_time

urlpatterns = [
    path('', views.home, name='home'),
    path("<int:id>", views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('myprofile/', views.myprofile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('purchase_ship/<int:ship_id>/', views.purchase_ship, name='purchase_ship'),
    path('config/', views.config, name='config'),
    path('api/get-time/', get_game_time, name='get-game-time'),
    path('invoice/<str:invoice_id>',views.invoice, name='invoice')
]