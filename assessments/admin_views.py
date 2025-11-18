from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import AssessmentForm, SectionForm, QuestionForm
from .models import Assessment, Section, Question


@staff_member_required
def add_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save()
            messages.success(request, 'Assessment created successfully.')
            return redirect('assessments-admin-add-question', assessment_id=assessment.id)
    else:
        form = AssessmentForm()
    return render(request, 'admin_add_assessment.html', {'form': form})


@staff_member_required
def add_question(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    sections = assessment.sections.all()
    if request.method == 'POST':
        qform = QuestionForm(request.POST)
        section_id = request.POST.get('section_select')
        new_section_title = request.POST.get('new_section_title')
        if qform.is_valid():
            # determine section
            if section_id:
                try:
                    section = Section.objects.get(id=int(section_id), assessment=assessment)
                except Exception:
                    section = None
            else:
                section = None

            if not section and new_section_title:
                section = Section.objects.create(assessment=assessment, title=new_section_title)

            question = qform.save(commit=False)
            if section:
                question.section = section
            question.save()
            messages.success(request, 'Question added successfully.')
            return redirect('assessments-admin-add-question', assessment_id=assessment.id)
    else:
        qform = QuestionForm()
    # fetch questions grouped by section for the template
    questions = Question.objects.filter(section__assessment=assessment).select_related('section')
    return render(request, 'admin_add_question.html', {
        'assessment': assessment,
        'sections': sections,
        'form': qform,
        'questions': questions,
    })


@staff_member_required
def delete_question(request, question_id):
    """Delete a question (POST only)."""
    question = get_object_or_404(Question, id=question_id)
    assessment = question.section.assessment if question.section else None
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        if assessment:
            return redirect('assessments-admin-add-question', assessment_id=assessment.id)
        return redirect('assessments-admin-add')
    # If GET, show a simple confirmation page
    return render(request, 'admin_confirm_delete_question.html', {'question': question})
