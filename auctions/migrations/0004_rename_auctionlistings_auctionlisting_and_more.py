# Generated by Django 4.1 on 2022-08-27 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_remove_bids_listing"),
    ]

    operations = [
        migrations.RenameModel(old_name="AuctionListings", new_name="AuctionListing",),
        migrations.RenameModel(old_name="Bids", new_name="Bid",),
        migrations.RenameModel(old_name="Comments", new_name="Comment",),
        migrations.RenameField(
            model_name="auctionlisting", old_name="cathegory", new_name="category",
        ),
    ]
