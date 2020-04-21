# Generated by Django 3.0.5 on 2020-04-21 19:51

from django.db import migrations, models
import django.db.models.deletion
import minutes.models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaMeetingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minutes.Meeting')),
            ],
            bases=(models.Model, minutes.models.MeetingItemMixin),
        ),
        migrations.CreateModel(
            name='AgendaSubItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('agenda_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minutes.AgendaMeetingItem')),
            ],
            bases=(models.Model, minutes.models.AgendaSubItemMixin),
        ),
        migrations.RemoveField(
            model_name='agendaitem',
            name='meeting',
        ),
        migrations.AlterField(
            model_name='vote',
            name='decision',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='minutes.Decision'),
        ),
        migrations.DeleteModel(
            name='SubItem',
        ),
        migrations.AlterField(
            model_name='decision',
            name='agenda_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minutes.AgendaMeetingItem'),
        ),
        migrations.DeleteModel(
            name='AgendaItem',
        ),
    ]
