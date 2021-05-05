from django.contrib import admin
from django.contrib.postgres import fields
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget
from preferences.admin import PreferencesAdmin
from adminsortable2.admin import SortableAdminMixin
from .models.geography import Geography
from .models.category import Category
from .models.dataset_file import DatasetFile
from .models.cca_preference import CCAPreferences


class MapSlugMappingAdmin(admin.ModelAdmin):
    list_display = ('map', 'slug')


class GeographyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cca3', 'created_at', 'updated')
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


class DatasetFileInline(admin.StackedInline):
    model = DatasetFile
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

    class Media:
        js = ('/static/admin/js/show_geonode_layer.js', )


class DatasetFileAdmin(admin.ModelAdmin):
    list_display = (
        'category', 'label', 'func', 'geonode_layer', 'active'
    )


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'name_long', 'sidebar_main_menu', 'sidebar_sub_menu', 'dataset', 'online')

    list_display_links = ('name_long', )

    list_filter = (
        'online',
    )

    fieldsets = (
        (None, {
            'fields': ('geography', 'name_long', 'unit', 'online', 'sidebar_main_menu', 'sidebar_sub_menu', 'legend_range_steps')
        }),
        ('Advanced configurations', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('boundary_layer', 'analysis', 'controls', 'configuration', 'domain', 'domain_init', 'timeline', 'vectors', 'metadata'),
        }),
    )

    def dataset(self, obj):
        html = ''
        for dataset_file in obj.datasetfile_set.all():
            if dataset_file.use_geonode_layer:
                html += '<a href={} target="_blank"> <span class="badge badge-secondary">Layer</span> '.format(
                    dataset_file.geonode_layer.detail_url
                )
            else:
                html += '<a href={}>'.format(
                    dataset_file.endpoint.url
                )
            if dataset_file.label:
                html += dataset_file.label
            else:
                html += '{} file'.format(dataset_file.func)
            html += '</a>'
            html += '<br>'
        return format_html(html)

    dataset.short_description = 'Dataset'
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget(height='250px')},
    }
    inlines = [
        DatasetFileInline
    ]


admin.site.register(Geography, GeographyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DatasetFile, DatasetFileAdmin)
admin.site.register(CCAPreferences, PreferencesAdmin)
