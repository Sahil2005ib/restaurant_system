from django.urls import path
from . import views


urlpatterns = [

    path('login/', views.user_login, name='user_login'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),

    path('logout/', views.user_logout, name='logout'),

    path('menu/', views.menu_list, name='menu_list'),

    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),

    path('manager/inventory-approval/', views.inventory_approval_portal, name='inventory_approval_portal'),

    path('feedback/', views.feedback_form, name='feedback_form'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),

    path('reserve/', views.reservation_form, name='reservation_form'),
    path('reservation-success/<int:reservation_id>/', views.reservation_success, name='reservation_success'),

    path('order', views.order_form, name='order_form'),
    path('order-success/', views.order_success, name='order_success'),

    path('payment', views.payment_form, name='payment_form'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),

    path('staff/', views.staff_portal, name='staff_portal'),
    path('staff-success/', views.staff_success, name='staff_success'),

    path('inventory/', views.inventory_portal, name='inventory_portal'),
    path('inventory-success/', views.inventory_success, name='inventory_success'),
    path('request-restock/', views.request_restock, name='request_restock'),

    path('report/', views.report_portal, name='report_portal'),
    path('report-success/', views.report_success, name='report_success'),
    path('approve-shift-change/<int:request_id>/', views.approve_shift_change, name='approve_shift_change'),
    path('reject-shift-change/<int:request_id>/', views.reject_shift_change, name='reject_shift_change'),
    path('approve-shift-swap/<int:request_id>/', views.approve_shift_swap, name='approve_shift_swap'),
    path('reject-shift-swap/<int:request_id>/', views.reject_shift_swap, name='reject_shift_swap'),
    path('approve-sick-report/<int:report_id>/', views.approve_sick_report, name='approve_sick_report'),
    path('reject-sick-report/<int:report_id>/', views.reject_sick_report, name='reject_sick_report'),
]
