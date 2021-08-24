# Generated by Django 3.2.4 on 2021-08-24 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptid',
            name='description',
            field=models.TextField(max_length=150),
        ),
        migrations.AlterField(
            model_name='cryptid',
            name='location',
            field=models.CharField(max_length=150),
        ),
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_of_day', models.CharField(choices=[('A', 'Dawn'), ('B', 'Morning'), ('C', 'Midday'), ('D', 'Afternoon'), ('E', 'Dusk'), ('F', 'Evening'), ('G', 'Midnight')], default='A', max_length=1)),
                ('notes', models.TextField(max_length=150)),
                ('cryptid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.cryptid')),
            ],
        ),
    ]