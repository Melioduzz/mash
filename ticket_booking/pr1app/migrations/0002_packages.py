# Generated by Django 3.2.23 on 2023-12-05 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pr1app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Packages_date', models.CharField(max_length=250)),
                ('Packages_name', models.CharField(max_length=250)),
                ('Packages_price', models.CharField(max_length=250)),
                ('Packages_desc', models.TextField()),
                ('Packages_img', models.ImageField(upload_to='pics')),
            ],
        ),
    ]