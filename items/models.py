from django.db import models

class ItemShop(models.Model):
    nft_id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    rental_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)