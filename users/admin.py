from django.contrib import admin
from django.contrib.auth.models import User
from .models import ParentProfile, ChildProfile
from django.http import HttpResponse
import csv


class ChildInline(admin.TabularInline):
    model = ChildProfile
    extra = 0
    fields = ('first_name', 'last_name', 'dob', 'gender', 'grade')


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'consent_given', 'locale', 'child_count')
    search_fields = ('user__username', 'user__email')
    inlines = [ChildInline]
    fieldsets = (
        (None, {'fields': ('user', 'phone')}),
        ('Consent', {'fields': ('consent_given', 'consent_date')}),
        ('Localization', {'fields': ('locale',)}),
    )
    readonly_fields = ('child_count',)
    actions = ['export_as_csv']

    def child_count(self, obj):
        return obj.children.count()
    child_count.short_description = 'Number of Children'

    def export_as_csv(self, request, queryset):
        field_names = ['id', 'user', 'phone', 'consent_given', 'consent_date', 'locale', 'child_count']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=parents.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([obj.id, obj.user.username, obj.phone, obj.consent_given, obj.consent_date, obj.locale, obj.children.count()])
        return response

    export_as_csv.short_description = 'Export selected parents as CSV'

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff


@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'parent', 'dob', 'grade')
    search_fields = ('first_name', 'last_name', 'parent__user__username')
    list_filter = ('grade',)
    fieldsets = (
        (None, {'fields': ('parent', 'first_name', 'last_name')}),
        ('Details', {'fields': ('dob', 'gender', 'grade', 'avatar_url')}),
        ('Notes', {'fields': ('notes',)}),
    )

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        field_names = ['id', 'first_name', 'last_name', 'parent', 'dob', 'gender', 'grade']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=children.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([obj.id, obj.first_name, obj.last_name, obj.parent.id if obj.parent else '', obj.dob, obj.gender, obj.grade])
        return response

    export_as_csv.short_description = 'Export selected children as CSV'

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff
