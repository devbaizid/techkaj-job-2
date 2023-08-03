from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/proposals/create/', views.create_proposal, name='create_proposal'),
    path('proposals/<int:proposal_id>/hire/', views.hire_freelancer, name='hire_freelancer'),
    path('proposal/reject/<int:proposal_id>/', views.proposal_rejecte, name='proposal_rejecte'),
    path('login/',views.login_view, name="login"),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/',views.Dashboard, name="dashboard"),
    path('about/',views.about, name="about"),
path('contact/',views.contact, name="contact"),
path('service/',views.service_view, name="service"),


path('send_files/<int:proposal_id>/',views.Send_projects_file_view,name="file_send"),


path('payout/<int:proposal_id>/', views.payout, name='payout'),

    path('bkash/<int:payout_id>/update/', views.e_bkash, name='e_bkash'),
    path('bank/<int:payout_id>/update/', views.e_bank, name='e_bank'),
    path('paypal/<int:payout_id>/update/', views.e_paypal, name='e_paypal'),





]
