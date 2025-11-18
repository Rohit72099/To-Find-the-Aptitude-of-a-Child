from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('children/', views.children_list, name='children-list'),
    path('children/add/', views.children_add, name='children-add'),
    # Legacy/alternate URL pattern used by some links: /children/edit/<id>/
    path('children/edit/<int:child_id>/', views.children_edit, name='children-edit-legacy'),
    path('children/<int:child_id>/edit/', views.children_edit, name='children-edit'),
    path('children/<int:child_id>/assessments/', views.children_assessments, name='children-assessments'),
    path('assessments/', views.assessments_list, name='assessments-list'),
    path('test/', views.test_taking, name='test-taking'),
    path('assessments/<int:assessment_id>/start/', views.test_start, name='test-start'),
    path('results/', views.results_list, name='results-list'),
    path('results/<uuid:session_id>/', views.results, name='results'),
]

