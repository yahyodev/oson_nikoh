from django.db import models


class TimeBasedModel(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date of creation",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="date of last modification",
    )

    class Meta:
        abstract = True


class User(TimeBasedModel):
    class Meta:
        verbose_name = ("Dating User",)
        verbose_name_plural = "Dating Users"

    id = models.AutoField(primary_key=True)
    telegram_id = models.PositiveBigIntegerField(
        unique=True, default=1, verbose_name="telegram id"
    )
    status = models.BooleanField(default=False, verbose_name='status')
    is_fake = models.BooleanField(default=False, verbose_name='is fake', null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name='active')
    full_name = models.CharField(max_length=255, verbose_name="full name", null=True, blank=True)

    phone_number = models.BigIntegerField(
        verbose_name="phone number", null=True, blank=True
    )
    name = models.CharField(max_length=255, verbose_name="name")
    username = models.CharField(max_length=255, verbose_name="telegram username", null=True, blank=True)
    age = models.IntegerField(verbose_name='age', null=True, blank=True)
    sex = models.CharField(
        max_length=30, verbose_name="user's sex", null=True, blank=True
    )
    location = models.CharField(
        max_length=255, verbose_name="user's location", null=True, blank=True
    )
    height = models.IntegerField(verbose_name='height', null=True, blank=True)
    weight = models.IntegerField(verbose_name='weight', null=True, blank=True)
    ethnicity = models.CharField(max_length=255, verbose_name='ethnicity', null=True, blank=True)
    marital_status = models.CharField(max_length=255, verbose_name='marital status', null=True, blank=True)
    education = models.CharField(max_length=255, verbose_name='education', null=True, blank=True)
    occupation = models.CharField(max_length=255, verbose_name='occupation', null=True, blank=True)
    biography = models.TextField(verbose_name='biography', null=True, blank=True)
    photo_id = models.CharField(max_length=400, verbose_name="Photo_ID", null=True)

    need_partner_age_min = models.PositiveIntegerField(
        verbose_name="minimum partner age", default=18
    )
    need_partner_age_max = models.PositiveIntegerField(
        verbose_name="maximum partner age", default=78
    )

    viewed_profiles = models.ManyToManyField(
        "self", through="ViewedProfile", symmetrical=False
    )

    def __str__(self):
        return f"№{self.id} ({self.telegram_id}) - {self.name}"


class ViewedProfile(models.Model):
    viewer = models.ForeignKey(User, related_name="viewer", on_delete=models.CASCADE)
    profile = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    liked = models.BooleanField(default=False, verbose_name="liked")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("viewer", "profile")
