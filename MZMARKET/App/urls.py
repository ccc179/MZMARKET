from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),

    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_params, name='market_with_params'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),

    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^checkuser/', views.check_user, name='check_user'),
    url(r'^logout/', views.log_out, name='log_out'),

    url(r'^activate/', views.activate, name='activate'),

    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
    url(r'^changecartstate/', views.change_cart_state, name='change_cart_state'),
    url(r'^subfromcart/', views.sub_from_cart, name='sub_from_cart'),
    url(r'^allselect/', views.all_select, name='all_select'),
    url(r'^subfrommarket/', views.sub_from_market, name='sub_from_market'),

    url(r'^makeorder/', views.make_order, name='make_order'),
    url(r'^orderdetail/', views.order_detail, name='order_detail'),
]
