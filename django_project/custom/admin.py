from django.contrib import admin
from django.contrib.postgres import fields
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget
from preferences.admin import PreferencesAdmin
from adminsortable2.admin import SortableAdminMixin
from geonode.layers.models import Layer

from .models import SummaryReportResult, SummaryReportCategory, \
    SummaryReportDataset, MapImage
from .models.geography import Geography
from .models.category import Category
from .models.dataset_file import DatasetFile
from .models.cca_preference import CCAPreferences
from .models.unit import Unit
from .models.menu import *
from custom.models.preset import Preset
from custom.models.use_case import UseCase
from custom.models.clipped_layer import ClippedLayer


class MapSlugMappingAdmin(admin.ModelAdmin):
    list_display = ('map', 'slug')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', ]


class GeographyAdmin(admin.ModelAdmin):
    change_form_template = 'admin/custom/geography/change_form.html'

    list_display = ('name', 'cca3', 'created_at', 'vector_boundary_layer')
    exclude = ('configuration', 'circle', 'pack', 'parent', 'adm',
               'boundary_dimension_x', 'boundary_dimension_y',
               'created_by', 'updated_by', 'boundary_file')
    search_fields = ('name', )
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

    autocomplete_fields = [
        'household_layer', 'urban_layer', 'cooking_percentage_layer',
        'wealth_index_layer']

    def get_form(self, request, obj=None, **kwargs):
        form = super(GeographyAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['vector_boundary_layer'].queryset = (
            Layer.objects.filter(
                storeType__contains='dataStore')
        )
        form.base_fields['raster_mask_layer'].queryset = Layer.objects.filter(
            storeType__contains='coverageStore')
        return form

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()


class DatasetFileInline(admin.StackedInline):
    model = DatasetFile
    autocomplete_fields = ['geonode_layer', ]
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0
    max_num = 3

    class Media:
        js = ('/static/admin/js/show_geonode_layer.js', )


class DatasetFileAdmin(admin.ModelAdmin):
    list_display = (
        'category', 'label', 'func', 'geonode_layer', 'active'
    )


class MainMenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    autocomplete_fields = ['geography', ]
    search_fields = ('name', )
    list_display = ('name', 'geography')


class SubMenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    autocomplete_fields = ['main_menu', ]
    search_fields = ('name', 'main_menu__name')
    list_display = ('name', 'main_menu')


class PresetAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', )


class UseCaseAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'geography', 'description')
    search_fields = ('name', 'geography')
    list_filter = ('geography', )


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'name_long', 'sidebar_sub_menu_obj', 'dataset', 'online')

    search_fields = ('name_long', )

    autocomplete_fields = ['unit_object', 'sidebar_sub_menu_obj' ]

    list_display_links = ('name_long', )

    list_filter = (
        'online',
        'sidebar_sub_menu_obj'
    )

    fieldsets = (
        (None, {
            'classes': ('main-module', ),
            'fields': ('geography', 'name_long', 'unit_object', 'online', 'sidebar_sub_menu_obj')
        }),
        ('EAP', {
            'classes': ('grp-collapse hidden-fieldset eap-fieldset',),
            'fields': ('eap_use', 'eap_scale', 'eap_invert'),
        }),
        ('Demand', {
            'classes': ('grp-collapse hidden-fieldset demand-fieldset',),
            'fields': ('demand_index', 'demand_scale', 'demand_invert'),
        }),
        ('Supply', {
            'classes': ('grp-collapse hidden-fieldset supply-fieldset',),
            'fields': ('supply_index', 'supply_scale', 'supply_invert'),
        }),
        ('ANI', {
            'classes': ('grp-collapse hidden-fieldset supply-fieldset',),
            'fields': ('ani_index', 'ani_scale', 'ani_invert'),
        }),
        ('Advanced configurations', {
            'classes': ('grp-collapse grp-closed advanced-module',),
            'fields': ('boundary_layer', 'legend_range_steps', 'range_type', 'weight',
                       'analysis', 'domain', 'domain_init', 'timeline', 'vectors', 'metadata'),
        }),
    )

    def dataset(self, obj):
        html = ''
        for dataset_file in obj.datasetfile_set.all():
            dataset_found = False
            if dataset_file.use_geonode_layer and dataset_file.geonode_layer:
                html += '<a href={} target="_blank"> <span class="badge badge-secondary">Layer</span> '.format(
                    dataset_file.geonode_layer.detail_url
                )
                dataset_found = True
            elif dataset_file.endpoint:
                html += '<a href={}>'.format(
                    dataset_file.endpoint.url
                )
                dataset_found = True
            if dataset_found:
                if dataset_file.label:
                    html += dataset_file.label
                else:
                    html += '{} file'.format(dataset_file.func)
                html += '</a>'
            else:
                html += '-'
            html += '<br>'
        return format_html(html)

    dataset.short_description = 'Dataset'
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget(height='250px')},
    }
    inlines = [
        DatasetFileInline
    ]

    class Media:
        js = ('/static/admin/js/category.js', )


class ClippedLayerAdmin(admin.ModelAdmin):
    list_filter = ('layer_type', )
    search_fields = ('boundary_uuid', 'layer__name')
    list_display = (
        'layer', 'boundary_uuid', 'created_date',
        'layer_type', 'state')


class SummaryReportResultAdmin(admin.ModelAdmin):
    list_display = (
       'summary_report_category', 'analysis', 'boundary_uuid',
       'created_at', 'dataset_file'
    )


class SummaryReportCategoryAdmin(admin.ModelAdmin):
    change_form_template = 'admin/custom/summary_report_category/change_form.html'
    autocomplete_fields = ['vector_layer', ]
    list_display = (
       'name', 'analysis', 'preset', 'vector_layer', 'supply_layer',
    )
    list_filter = (
        'analysis',
        'preset'
    )
    search_fields = (
        'name',
        'analysis',
        'preset__name'
    )

    class Media:
        js = ('/static/admin/js/summary_report_category.js', )

    def get_form(self, request, obj=None, **kwargs):
        form = super(SummaryReportCategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['supply_layer'].queryset = Layer.objects.filter(
            storeType__contains='coverageStore')
        return form


class MapImageAdmin(admin.ModelAdmin):
    list_filter = ('preset',)
    list_display = (
        'preset', 'image', 'geonode_layer',
        'created_at')


admin.site.register(Geography, GeographyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CCAPreferences, PreferencesAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(MainMenu, MainMenuAdmin)
admin.site.register(SubMenu, SubMenuAdmin)
admin.site.register(Preset, PresetAdmin)
admin.site.register(UseCase, UseCaseAdmin)
admin.site.register(ClippedLayer, ClippedLayerAdmin)
admin.site.register(SummaryReportResult, SummaryReportResultAdmin)
admin.site.register(SummaryReportCategory, SummaryReportCategoryAdmin)
admin.site.register(SummaryReportDataset)
admin.site.register(MapImage, MapImageAdmin)
