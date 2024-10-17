# Generated by Django 5.1.2 on 2024-10-15 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]