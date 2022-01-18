# Generated by Django 3.2.10 on 2022-01-18 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='illness',
            name='to_patient_illness',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='illnesses', to='api.patientillnesses'),
        ),
        migrations.AlterField(
            model_name='patientillnesses',
            name='to_discharge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='illnesses', to='api.discharge'),
        ),
        migrations.AlterField(
            model_name='patientstates',
            name='to_discharge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='api.discharge'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='to_discharge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='api.discharge'),
        ),
    ]
