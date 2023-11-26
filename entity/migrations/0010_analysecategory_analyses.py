# Generated by Django 4.1.6 on 2023-11-13 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0009_alter_hospital_assigneduser'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses_categories', to='entity.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Analyses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('price', models.FloatField()),
                ('code', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='entity.analysecategory')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='entity.hospital')),
            ],
        ),
    ]