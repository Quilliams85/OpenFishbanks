from django.urls import path
from . import views
from .views import get_game_time
from register.views import settings_view

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('myprofile/', views.myprofile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('purchase_ship/<int:ship_id>/', views.purchase_ship, name='purchase_ship'),
    path('config/', views.config, name='config'),
    path('api/get-time/', get_game_time, name='get-game-time'),
    path('invoice/<str:invoice_id>',views.invoice, name='invoice'),
    path('modify/<str:ship_id>', views.modify, name='modify'),
    path('invoices', views.invoice_list, name='invoice_list'),
    path('finances', views.user_finances, name='user_finances'),
    path('about', views.about, name='about'),
    path('inventory', views.user_inventory, name='inventory'),
    path('transactions', views.user_transactions, name='transactions'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/add_member/', views.add_member, name='add_member'),
    path('groups', views.user_groups, name='groups'),
    path('group/<int:organization_id>/', views.group_detail, name='group_detail'),
    path('invitation/accept/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),
    path('invitation/decline/<int:invitation_id>/', views.decline_invitation, name='decline_invitation'),
    path('group/<int:group_id>/leave', views.leave_group, name='leave_group'),
    path('group/<int:group_id>/delete', views.delete_group, name='delete_group'),
    path('create_listing/<str:ship_id>', views.create_listing, name='create_listing'),
    path('buy_now/<int:auction_id>', views.buy_now, name='buy_now'),
    path('bid/<int:auction_id>/', views.place_bid, name='place_bid'),
    path('harbors/', views.harbors, name='harbors'),
    path('harbors/<int:harbor_id>', views.harbor_detail, name='harbor_detail'),
    path('market/', views.fish_market, name='fish_market'),
    path('trade/create/', views.create_trade_request, name='create_trade'),
    path('trade/', views.view_trades, name='view_trades'),
    path('trade/respond/<int:trade_id>/<str:response>/', views.respond_to_trade, name='respond_to_trade'),
    path('settings/', settings_view, name='settings'),
    path('api/get-species', views.export_fish_data_csv, name='get_species'),
    path('api/get-leaderboard', views.api_leaderboard, name='get_leaderboard'),
    path('net-leaderboard', views.net_worth_leaderboard, name='net_leaderboard'),
    path('api/get-users', views.get_user_data, name='get_user_data'),
    path('api/get-fish-values', views.get_fish_data, name='get_fish_data'),
]
