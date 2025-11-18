from django.urls import path
from .views import AssessmentListView, AssessmentDetailView, start_assessment, submit_answer, complete_assessment, get_results

from .views import get_user_results
from . import admin_views

urlpatterns = [
    path('results/', get_user_results, name='user-results'),
    path('assessments/', AssessmentListView.as_view(), name='assessments-list'),
    path('assessments/<int:pk>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    path('assessments/<int:assessment_id>/start/', start_assessment, name='assessment-start'),
    path('sessions/', start_assessment, name='sessions-list'),
    path('sessions/<uuid:session_id>/answer/', submit_answer, name='session-answer'),
    path('sessions/<uuid:session_id>/complete/', complete_assessment, name='session-complete'),
    path('sessions/<uuid:session_id>/results/', get_results, name='session-results'),
    # Staff-friendly admin pages
    path('admin/add/', admin_views.add_assessment, name='assessments-admin-add'),
    path('admin/<int:assessment_id>/questions/add/', admin_views.add_question, name='assessments-admin-add-question'),
    path('admin/question/<int:question_id>/delete/', admin_views.delete_question, name='assessments-admin-delete-question'),
]
