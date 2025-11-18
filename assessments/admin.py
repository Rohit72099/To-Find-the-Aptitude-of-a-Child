from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Assessment, Section, Question, Result, Response, ScoringRule


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ('text', 'type', 'order', 'difficulty', 'time_limit')


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    fields = ('title', 'order')


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'age_min', 'age_max', 'time_limit', 'adaptive', 'published', 'version')
    search_fields = ('title', 'description')
    list_filter = ('language', 'published', 'adaptive')
    inlines = [SectionInline]
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Targeting', {'fields': ('age_min', 'age_max', 'language', 'version')}),
        ('Options', {'fields': ('time_limit', 'adaptive', 'published')}),
    )
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        """Export selected Assessments as CSV."""
        meta = self.model._meta
        field_names = ['id', 'title', 'language', 'age_min', 'age_max', 'time_limit', 'adaptive', 'published', 'version']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=assessments.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, f) for f in field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = "Export selected assessments as CSV"

    # Explicit staff-only enforcement (Django admin already requires is_staff, but make explicit)
    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'assessment', 'order')
    search_fields = ('title',)
    inlines = [QuestionInline]
    fieldsets = (
        (None, {'fields': ('assessment', 'title', 'order')}),
    )
    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'section', 'type', 'order', 'difficulty', 'options_preview')
    search_fields = ('text',)
    list_filter = ('type',)
    fieldsets = (
        (None, {'fields': ('section', 'text', 'type')}),
        ('Settings', {'fields': ('order', 'difficulty', 'time_limit', 'media_url')}),
    )
    actions = ['export_as_csv']

    def options_preview(self, obj):
        try:
            opts = obj.options or {}
            options_list = opts.get('options') if isinstance(opts, dict) else opts
            if isinstance(options_list, list):
                return ', '.join(str(x) for x in options_list[:5])
        except Exception:
            return ''
        return ''
    options_preview.short_description = 'Options'

    def export_as_csv(self, request, queryset):
        field_names = ['id', 'section', 'type', 'order', 'difficulty']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=questions.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([obj.id, obj.section.id if obj.section else '', obj.type, obj.order, obj.difficulty])
        return response

    export_as_csv.short_description = 'Export selected questions as CSV'

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def short_text(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text
    short_text.short_description = 'Question'


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    readonly_fields = ('question', 'answer', 'correct', 'time_taken')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'child', 'assessment', 'completed_at', 'percent_score')
    search_fields = ('id', 'child__first_name', 'child__last_name', 'assessment__title')
    list_filter = ('assessment',)
    readonly_fields = ('started_at', 'completed_at', 'raw_scores', 'normalized_scores', 'recommendations', 'percent_score')
    inlines = [ResponseInline]
    actions = ['export_as_csv']

    fieldsets = (
        (None, {'fields': ('id', 'child', 'assessment')}),
        ('Timestamps', {'fields': ('started_at', 'completed_at')}),
        ('Scores', {'fields': ('raw_scores', 'normalized_scores', 'percent_score')}),
        ('Extras', {'fields': ('recommendations',)}),
    )

    def percent_score(self, obj):
        try:
            return obj.normalized_scores.get('percent') if obj.normalized_scores else None
        except Exception:
            return None
    percent_score.short_description = 'Percent Score'

    def export_as_csv(self, request, queryset):
        field_names = ['id', 'child', 'assessment', 'completed_at', 'percent']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=results.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            percent = None
            try:
                percent = obj.normalized_scores.get('percent') if obj.normalized_scores else None
            except Exception:
                percent = None
            writer.writerow([obj.id, obj.child.id if obj.child else '', obj.assessment.id if obj.assessment else '', obj.completed_at, percent])
        return response

    export_as_csv.short_description = 'Export selected results as CSV'

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff


@admin.register(ScoringRule)
class ScoringRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessment')
    search_fields = ('assessment__title',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('result', 'question', 'correct', 'time_taken')
    search_fields = ('question__text',)
    readonly_fields = ('answer',)
