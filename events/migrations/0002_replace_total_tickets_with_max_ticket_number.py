from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffleevent',
            name='max_ticket_number',
            field=models.PositiveIntegerField(
                default=60,
                help_text='Highest allowed ticket number (e.g. 60 means tickets 1\u201360)'
            ),
        ),
    ]
