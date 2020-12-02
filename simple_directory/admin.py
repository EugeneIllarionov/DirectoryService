from django.contrib import admin
from simple_directory.models import DirectoryItem, Directory, DirectoryBase


@admin.register(DirectoryItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'value')
    search_fields = ('code', 'value')


class DirectoryAdminInline(admin.TabularInline):

    model = Directory
    extra = 1
    can_delete = True
    show_change_link = True


@admin.register(DirectoryBase)
class DirectoryBaseAdmin(admin.ModelAdmin):

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        return super(DirectoryBaseAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    # readonly_fields = ['start_date']
    # fields = ('name', 'short_name', 'description',)
    inlines = (DirectoryAdminInline,)
    list_display = ('id', 'short_name', 'description', 'last_version' )




