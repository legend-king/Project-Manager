from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableStackedInline, SortableAdminBase
from .models import Project, ProjectModule, ModuleTask
# Register your models here.

class ModuleTaskInline(admin.StackedInline):
    model = ModuleTask
    extra = 1

class ProjectModuleInline(admin.TabularInline):
    model = ProjectModule
    extra = 1
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status','due_date']
    search_fields = ['title', 'description']
    list_editable = ['priority', 'status']
    list_filter = ['priority', 'status', 'due_date']
    fields = ['title', 'description','github_link','priority', 'status', 'due_date']
    inlines = [ProjectModuleInline]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs
    


@admin.register(ProjectModule)
class ProjectModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'priority', 'completed', 'due_date']
    search_fields = ['title', 'description', 'project__title']
    list_filter = ['project', 'priority', 'completed']
    list_editable = ['priority', 'completed']
    autocomplete_fields = ['project']
    inlines = [ModuleTaskInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(project__user=request.user)
        return qs

@admin.register(ModuleTask)
class ModuleTaskAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = ['my_order']
    list_display = ['title', 'module', 'completed', 'due_date', 'my_order']
    search_fields = ['title']
    list_filter = ['module', 'completed']
    list_editable = ['completed']
    autocomplete_fields = ['module']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(module__project__user=request.user)
        return qs
