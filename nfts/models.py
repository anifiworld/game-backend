from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


# class Nfts(models.Model):
#     nft_id = models.CharField(max_length=255, unique=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nfts")
#     amount = models.IntegerField(default=1)

#     def __str__(self) -> str:
#         return f"nft {self.nft_id} user {self.user} amount {self.amount}"

#     class Meta:
#         unique_together = ("nft_id", "user")


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class ItemBalance(models.Model):
    address = models.CharField(max_length=255)
    resource = models.CharField(max_length=255)
    balance = models.CharField(max_length=255)
    is_on_chain = models.BooleanField(
        db_column="isOnChain"
    )  # Field name made lowercase.
    expiration_date = models.IntegerField(
        db_column="expirationDate", blank=True, null=True
    )  # Field name made lowercase.
    created_at = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updated_at = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "indexer_item_balances"
        unique_together = (("address", "resource"),)
