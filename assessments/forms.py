from django import forms
from .models import Assessment, Section, Question
import json


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'age_min', 'age_max', 'language', 'time_limit', 'adaptive', 'published', 'version']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'order']


class QuestionForm(forms.ModelForm):
    # options_input will accept JSON or simple comma-separated options
    options_input = forms.CharField(widget=forms.Textarea, required=False, help_text='Enter JSON like {"options": ["A","B"], "correct": 1} or comma-separated options')

    class Meta:
        model = Question
        fields = ['text', 'type', 'order', 'difficulty', 'time_limit', 'media_url']

    def clean_options_input(self):
        data = self.cleaned_data.get('options_input')
        if not data:
            return None
        try:
            # First try JSON
            parsed = json.loads(data)
            return parsed
        except Exception:
            # Fallback: comma-separated values
            parts = [p.strip() for p in data.split(',') if p.strip()]
            return {'options': parts}

    def save(self, commit=True):
        obj = super().save(commit=False)
        opts = self.cleaned_data.get('options_input')
        if opts:
            obj.options = opts
        if commit:
            obj.save()
        return obj
