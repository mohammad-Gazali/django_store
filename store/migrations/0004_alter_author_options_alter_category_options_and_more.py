# Generated by Django 4.1 on 2022-09-11 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_product_pdf_file"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="author",
            options={"verbose_name": "الكاتب", "verbose_name_plural": "الكتاب"},
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "الفئة", "verbose_name_plural": "الفئات"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "المنتج", "verbose_name_plural": "المنتجات"},
        ),
        migrations.AlterModelOptions(
            name="slider",
            options={"verbose_name": "الشريحة", "verbose_name_plural": "الشرائح"},
        ),
    ]
