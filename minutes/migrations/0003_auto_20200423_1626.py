# Generated by Django 3.0.5 on 2020-04-23 16:26

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import minutes.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
        ('minutes', '0002_auto_20200421_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('decision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='minutes.Decision')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, minutes.models.VoteMixin),
        ),
        migrations.CreateModel(
            name='RollCallVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rollcall_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MinutesUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='votechoice',
            name='color_code',
            field=models.IntegerField(default=16711680),
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.AddField(
            model_name='anonymousvote',
            name='vote_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='used_by', to='minutes.VoteChoice'),
        ),
    ]
