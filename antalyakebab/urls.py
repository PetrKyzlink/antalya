from django.urls import path
from . import views
from . import url_handler

urlpatterns = [
    # customer
    path("nabidka/", views.menu, name="nabidka"),
    path("", url_handler.menu_handler),
    path("kosik/", views.cart, name="kosik"),
    path("objednavka/", views.checkout, name="objednavka"),
    path("objednavka-odeslana/", views.order_sent, name="objednavka-odeslana"),
    path("neco-se-nepovedlo/", views.something_wrong, name="neco-se-nepovedlo"),
    path("cookies-nesouhlas/", views.unapproved_cookies, name="cookies-nesouhlas"),
    path("rozvoz-nedostupny/", views.closed, name="rozvoz-nedostupny"),

    path('reject_cookies/', views.rejectCookies, name='reject_cookies'),
    path('accept_cookies/', views.acceptCookies, name='accept_cookies'),
    path("update_item/", views.updateItem, name="update_item"),
    path("update_delivery/", views.updateDelivery, name="update_delivery"), 

    # service
    path("obsluha/", views.service, name="obsluha"),
    path("historie-objednavek/", views.history_orders, name="historie-objednavek"),
    path('nova-objednavka-detail/<int:pk>/<str:order_number>/', views.new_order_detail, name='nova-objednavka-detail'),
    path('dnes-vyrizena-objednavka-detail/<int:pk>/<str:order_number>/', views.today_completed_order_detail, name='dnes-vyrizena-objednavka-detail'),
    path('historie-objednavka-detail/<int:pk>/<str:order_number>/', views.history_order_detail, name='historie-objednavka-detail'),

    path('close-page-new-orders/', views.close_page_new_orders, name='close-page-new-orders'),
    path('close-page-today-orders-completed/', views.close_page_today_orders_completed, name='close-page-today-orders-completed'),
    path('close-page-history-order/<int:pk>/', views.close_page_history_order, name='close-page-history-order'),

    path('new_order_confirmation/', views.newOrderConfirmation, name='new_order_confirmation'),
    path('order_completed/', views.orderCompleted, name='order_completed'),
    path('order_cancellation/', views.orderCancellation, name='order_cancellation'),

]
