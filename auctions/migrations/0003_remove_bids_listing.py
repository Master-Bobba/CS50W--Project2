# Generated by Django 4.1 on 2022-08-27 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_auctionlistings_comments_bids"),
    ]

    operations = [
        migrations.RemoveField(model_name="bids", name="listing",),
    ]
