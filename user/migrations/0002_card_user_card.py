# Generated by Django 4.2.2 on 2023-07-08 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardNum', models.CharField(max_length=100, unique=True)),
                ('csv', models.SmallIntegerField()),
                ('lastDate', models.SmallIntegerField()),
                ('activeCard', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card', to='user.card'),
        ),
    ]
