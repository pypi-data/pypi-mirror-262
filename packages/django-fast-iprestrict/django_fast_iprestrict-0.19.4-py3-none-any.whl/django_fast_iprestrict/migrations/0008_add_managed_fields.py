# Generated by Django 5.0.1 on 2024-01-30 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_fast_iprestrict", "0007_ruleratelimitgroup_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="rule",
            name="managed_fields",
            field=models.JSONField(blank=True, default=list, editable=False),
        ),
        migrations.AddField(
            model_name="rulenetwork",
            name="managed_fields",
            field=models.JSONField(blank=True, default=list, editable=False),
        ),
        migrations.AddField(
            model_name="rulepath",
            name="managed_fields",
            field=models.JSONField(blank=True, default=list, editable=False),
        ),
        migrations.AddField(
            model_name="ruleratelimit",
            name="managed_fields",
            field=models.JSONField(blank=True, default=list, editable=False),
        ),
        migrations.AddField(
            model_name="ruleratelimitgroup",
            name="managed_fields",
            field=models.JSONField(blank=True, default=list, editable=False),
        ),
        migrations.AddField(
            model_name="rulesource",
            name="managed_fields",
            field=models.JSONField(blank=True, default=list, editable=False),
        ),
    ]
