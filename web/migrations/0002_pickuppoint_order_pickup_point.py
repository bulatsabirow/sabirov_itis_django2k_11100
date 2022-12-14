# Generated by Django 4.1.2 on 2022-10-12 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickupPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('locality', models.CharField(max_length=500)),
            ],
            options={
                'unique_together': {('address', 'locality')},
            },
        ),
        migrations.AddField(
            model_name='order',
            name='pickup_point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.pickuppoint'),
        ),
    ]
