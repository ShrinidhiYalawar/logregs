from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.expense_list, name='expense-list'),
    path('add/', views.add_expense, name='add-expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit-expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete-expense'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('register/', views.register_view, name='register'),
    path('custom-admin/register-user/', views.register_user, name='register-user'),
    path('custom-admin/add-title/', views.add_title, name='add-title'),
]
