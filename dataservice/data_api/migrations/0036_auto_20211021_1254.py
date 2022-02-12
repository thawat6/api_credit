# Generated by Django 3.2.8 on 2021-10-21 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0035_auto_20211021_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrier',
            name='carrier_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.carrierclass'),
        ),
        migrations.AlterField(
            model_name='carrier',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.location'),
        ),
        migrations.AlterField(
            model_name='carrierclass',
            name='dimension',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.dimension'),
        ),
        migrations.AlterField(
            model_name='carrierclass',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.unitofmeasure'),
        ),
        migrations.AlterField(
            model_name='dimension',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.unitofmeasure'),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.product'),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.unitofmeasure'),
        ),
        migrations.AlterField(
            model_name='location',
            name='coord',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.coord'),
        ),
        migrations.AlterField(
            model_name='mapoutway',
            name='distance_uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='data_api.unitofmeasure'),
        ),
        migrations.AlterField(
            model_name='mapoutway',
            name='output_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to', to='data_api.location'),
        ),
        migrations.AlterField(
            model_name='mapway',
            name='source_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source', to='data_api.location'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.product'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.unitofmeasure'),
        ),
        migrations.AlterField(
            model_name='product',
            name='dimension',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.dimension'),
        ),
    ]