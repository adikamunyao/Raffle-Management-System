from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE payments_payment RENAME COLUMN mpesa_reference TO bank_reference;",
            reverse_sql="ALTER TABLE payments_payment RENAME COLUMN bank_reference TO mpesa_reference;",
        ),
    ]
