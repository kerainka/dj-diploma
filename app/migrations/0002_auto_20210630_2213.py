# Generated by Django 3.1.12 on 2021-06-30 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='review',
        ),
        migrations.AddField(
            model_name='productreview',
            name='review_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.product', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]
