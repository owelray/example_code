import uuid

from django.db import models

__all__ = (
    'BaseModel',
)


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'{self.__class__.__name__} object ({self.id})'

    class Meta:
        abstract = True

    @staticmethod
    def get_choice_object(object_id, choices):
        if object_id or isinstance(object_id, int):
            return {
                'id': object_id,
                'name': dict(choices)[object_id]
            }
        return None