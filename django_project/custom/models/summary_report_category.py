from django.db import models
from geonode.layers.models import Layer
from custom.models.preset import Preset


class SummaryReportCategory(models.Model):

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    vector_layer = models.ForeignKey(
        Layer,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    boundary_uuid = models.CharField(
        max_length=255,
        default='',
        blank=True
    )

    preset = models.ForeignKey(
        Preset,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Summary Calculation Categories'
        verbose_name = 'Summary Calculation Category'
