import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel
# Create your models here.


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super(BaseModelManager, self).get_queryset().filter(is_deleted=False)


# Create your models here.
class BaseModel(TimeStampedModel):
    """Base model - have common fields to all models."""
    # unique key to each record
    # maintaining uuid as primary key can be expensive, hence we will use uuid as secondary key as external identifier.
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # deletion attributes
    is_deleted = models.BooleanField(default=False, db_index=True)

    # overriding django model managers
    objects = BaseModelManager()  # overriding the django's object manager to filter out deleted records.
    all_objects = models.Manager()  # exposing all the objects including the soft deleted records.

    def hard_delete(self, *args, **kwargs):
        """hard delete which exposes actual delete from database"""
        super(BaseModel, self).delete(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """soft delete enforced for all models """
        self.is_deleted = True
        super().save()

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % self.uuid

    def __str__(self):
        return "{}".format(self.uuid)
