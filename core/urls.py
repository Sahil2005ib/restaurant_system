from django.urls import path
from core import views

urlpatterns = [
    # Feedback routes
    path('feedback/', views.feedback_form, name='feedback_form'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),

    path('reserve/', views.reservation_form, name='reservation_form'),
    path('reservation-success/', views.reservation_success, name='reservation_success'),

    path('order', views.order_form, name='order_form'),
    path('order-success/', views.order_success, name='order_success'),

    path('payment', views.payment_form, name='payment_form'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),

    path('staff/', views.staff_portal, name='staff_portal'),
    path('staff-success/', views.staff_success, name='staff_success'),

    path('inventory/', views.inventory_portal, name='inventory_portal'),
    path('inventory-success/', views.inventory_success, name='inventory_success'),
    
]
