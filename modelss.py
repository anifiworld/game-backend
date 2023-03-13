# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class BaseColor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "base_color"


class BaseFruit(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)
    extinct_at = models.DateTimeField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    color = models.ForeignKey(BaseColor, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "base_fruit"


class CrawlerBlockProcessingLogs(models.Model):
    blocknumber = models.IntegerField(
        db_column="blockNumber", unique=True, blank=True, null=True
    )  # Field name made lowercase.
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "crawler_block_processing_logs"


class CrawlerLogRecords(models.Model):
    blocknumber = models.IntegerField(
        db_column="blockNumber", blank=True, null=True
    )  # Field name made lowercase.
    logidx = models.IntegerField(
        db_column="logIdx", blank=True, null=True
    )  # Field name made lowercase.
    txidx = models.IntegerField(
        db_column="txIdx", blank=True, null=True
    )  # Field name made lowercase.
    txhash = models.TextField(
        db_column="txHash", blank=True, null=True
    )  # Field name made lowercase.
    timestamp = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "crawler_log_records"
        unique_together = (("blocknumber", "logidx"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class HeroesGem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    nft_id = models.CharField(max_length=255)
    attribute_value = models.DecimalField(max_digits=8, decimal_places=2)
    attribute_is_percentage = models.BooleanField()
    level_needed = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    attribute = models.ForeignKey("HeroesGemattribute", models.DO_NOTHING)
    price = models.IntegerField()
    is_on_chain = models.BooleanField()

    class Meta:
        managed = False
        db_table = "heroes_gem"


class HeroesGemattribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "heroes_gemattribute"


class HeroesGemuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    gem_slot = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    gem = models.ForeignKey(HeroesGem, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    hero_nft_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "heroes_gemuser"


class HeroesHeroclass(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "heroes_heroclass"


class HeroesHeroinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nft_id = models.CharField(unique=True, max_length=255)
    team_slot = models.IntegerField()
    exp = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    hero = models.ForeignKey("HeroesHerotype", models.DO_NOTHING, blank=True, null=True)
    is_on_chain = models.BooleanField()
    rank = models.ForeignKey("HeroesHerorank", models.DO_NOTHING, blank=True, null=True)
    rarity = models.ForeignKey(
        "HeroesHerorarity", models.DO_NOTHING, blank=True, null=True
    )
    owner = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "heroes_heroinfo"


class HeroesHerorank(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.IntegerField(unique=True)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "heroes_herorank"


class HeroesHerorarity(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "heroes_herorarity"


class HeroesHerotype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    hp_multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    atk_multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    matk_multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    def_multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    aspd_multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    hero_class = models.ForeignKey(HeroesHeroclass, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "heroes_herotype"


class IndexerApprovalIndices(models.Model):
    contractaddress = models.CharField(
        db_column="contractAddress", max_length=255
    )  # Field name made lowercase.
    approveraddress = models.CharField(
        db_column="approverAddress", max_length=255
    )  # Field name made lowercase.
    balance = models.CharField(max_length=255)
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "indexer_approval_indices"
        unique_together = (("contractaddress", "approveraddress"),)


class IndexerBalanceCommits(models.Model):
    blocknumber = models.IntegerField(
        db_column="blockNumber"
    )  # Field name made lowercase.
    logidx = models.IntegerField(db_column="logIdx")  # Field name made lowercase.
    arridx = models.IntegerField(db_column="arrIdx")  # Field name made lowercase.
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "indexer_balance_commits"
        unique_together = (("blocknumber", "logidx", "arridx"),)


class IndexerHeroStats(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    str = models.IntegerField()
    int = models.IntegerField()
    vit = models.IntegerField()
    agi = models.IntegerField()
    rank = models.IntegerField()
    owner = models.CharField(max_length=255, blank=True, null=True)
    isdeleted = models.BooleanField(db_column="isDeleted")  # Field name made lowercase.
    isonchain = models.BooleanField(db_column="isOnChain")  # Field name made lowercase.
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "indexer_hero_stats"


class IndexerItemBalances(models.Model):
    address = models.CharField(max_length=255)
    resource = models.CharField(max_length=255)
    balance = models.CharField(max_length=255)
    expirationdate = models.IntegerField(
        db_column="expirationDate", blank=True, null=True
    )  # Field name made lowercase.
    isonchain = models.BooleanField(db_column="isOnChain")  # Field name made lowercase.
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "indexer_item_balances"
        unique_together = (("address", "resource"),)


class IndexerNftApprovalIndices(models.Model):
    approver = models.CharField(max_length=255)
    contract = models.CharField(max_length=255)
    scope = models.IntegerField(blank=True, null=True)
    approved = models.BooleanField()
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "indexer_nft_approval_indices"
        unique_together = (("approver", "contract"),)


class IndexerTokenCirculations(models.Model):
    resource = models.CharField(unique=True, max_length=255)
    circulation = models.CharField(max_length=255)
    minted = models.CharField(max_length=255)
    burned = models.CharField(max_length=255)
    staked = models.CharField(max_length=255)
    createdat = models.DateTimeField(
        db_column="createdAt"
    )  # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column="updatedAt"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "indexer_token_circulations"


class MetamaskauthWalletauthmodel(models.Model):
    public_address = models.TextField(primary_key=True)
    nonce = models.TextField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "metaMaskAuth_walletauthmodel"


class PlayersPlayer(models.Model):
    id = models.BigAutoField(primary_key=True)
    stamina_last_updated_value = models.DecimalField(max_digits=15, decimal_places=5)
    stamina_last_updated = models.DateTimeField()
    coin_pending = models.FloatField()
    coin_last_withdrawn = models.DateTimeField()
    is_banned = models.BooleanField()
    hero_slot5_expired = models.DateTimeField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    stage_current = models.ForeignKey("StagesStage", models.DO_NOTHING)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    gem_slot5_expired = models.DateTimeField()
    gem_slot5_max_lv = models.IntegerField()
    hero_slot5_max_lv = models.IntegerField()
    gold = models.IntegerField()
    address = models.CharField(max_length=255, blank=True, null=True)
    team_slot = models.JSONField()

    class Meta:
        managed = False
        db_table = "players_player"


class StagesStage(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "stages_stage"
