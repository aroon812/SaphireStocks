# Generated by Django 2.2.5 on 2020-02-20 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200218_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='avg',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='close',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='high',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='low',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='open',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockchange',
            name='avg',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockchange',
            name='close',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockchange',
            name='high',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockchange',
            name='low',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockchange',
            name='open',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
