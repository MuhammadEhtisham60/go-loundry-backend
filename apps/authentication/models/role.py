from django.db import models
from django.utils.text import slugify


class Permission(models.Model):
    """
    Model representing system-wide granular permissions.
    """

    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        db_table = "permissions"
        ordering = ["code"]

    def __str__(self) -> str:
        return f"{self.label} ({self.code})"


class Role(models.Model):
    """
    Model representing user roles (e.g. Super Admin, Support Agent).
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    permissions = models.ManyToManyField(Permission, related_name="roles", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "roles"
        ordering = ["name"]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            val = other.lower().replace("_", "").replace(" ", "")
            my_val = self.name.lower().replace("_", "").replace(" ", "")
            return my_val == val
        if other is None:
            return False
        # Fallback to standard Django model equality comparison
        if not isinstance(other, models.Model):
            return False
        return self.pk == other.pk

    def __hash__(self) -> int:
        return hash(self.pk)
