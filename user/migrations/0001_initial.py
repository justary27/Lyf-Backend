# Generated by Django 4.1.6 on 2023-02-25 16:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='LyfUser',
            fields=[
                ('start_date', models.DateTimeField(auto_created=True, default=django.utils.timezone.now, editable=False, verbose_name='Joined')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.CharField(editable=False, max_length=28, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=80, unique=True, verbose_name='Username')),
                ('is_pro_user', models.BooleanField(default=False, verbose_name='Lyf Pro')),
                ('is_beta_tester', models.BooleanField(default=False, verbose_name='Lyf Beta Tester')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Lyf Staff')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Lyf Admin')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
