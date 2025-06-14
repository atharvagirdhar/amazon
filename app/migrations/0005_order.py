# Generated by Django 5.2.1 on 2025-05-29 05:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_carts_qty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.AutoField(primary_key=True, serialize=False)),
                ('orderdate', models.DateField(auto_now_add=True)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('orderstatus', models.CharField(choices=[('Pending', 'Pending'), ('shipped', 'shipped'), ('delivered', 'delivered')], default='Pending', max_length=50)),
                ('paymentstatus', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=50)),
                ('orderamount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.address')),
                ('productid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.products')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
