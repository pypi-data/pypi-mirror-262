from typing import Dict, Optional, Sequence
from functools import lru_cache
from django.db import models
from django.utils.translation import pgettext_lazy, pgettext

from .query import TranslationQuerySet
from .utils import get_language_choices
from .conf import settings
from .magic import (
    MAGIC_TRANSLATION_ENTITY_FIELD,
    MAGIC_TRANSLATION_STORED_FIELD,
    MAGIC_TRANSLATION_CONTROL_FIELD,
    apply_magic_to_translation_model
)


__all__ = (
    'TRANSLATION_POSTFIX',
    'TRANSLATION_RELATED_NAME',
    'translated_model_uniques',
    'base_translated_model',
    'create_language_field',
    'create_entity_field',
    'create_translation_model',
    'create_translated_model',
)

EMPTY = object()
TRANSLATION_POSTFIX: str = 'Translation'
TRANSLATION_RELATED_NAME: str = 'translations'


def translated_model_uniques():
    return (
        ('language', 'entity'),
    )


def collect_model_fields(
    model: models.Model, fields: Sequence[str]
) -> Dict[str, models.Field]:
    return {
        field: model._meta.get_field(field).clone()
        for field in fields
    }


@lru_cache
def base_translated_model():
    class BaseTranslatedModel(models.Model):
        objects = TranslationQuerySet.as_manager()

        class Meta:
            abstract = True

        id = models.BigAutoField(
            primary_key=True, verbose_name=pgettext_lazy('pxd_lingua', 'ID')
        )

        def __str__(self):
            return (
                pgettext(
                    'pxd_lingua',
                    '"{language}" translation for #{entity_id} entity'
                )
                .format(language=self.language, entity_id=self.entity_id)
            )

    return BaseTranslatedModel


def create_language_field(
    default_language: Optional[str] = EMPTY,
    languages: Optional[Sequence] = EMPTY
):
    return models.CharField(
        verbose_name=pgettext_lazy('pxd_lingua', 'Language'),
        max_length=32, choices=(
            get_language_choices()
            if languages is EMPTY
            else languages
        ),
        default=(
            settings.DEFAULT_LANGUAGE
            if default_language is EMPTY
            else default_language
        ),
        null=False, blank=False,
    )


def create_entity_field(
    model: models.Model,
    related_name: str = TRANSLATION_RELATED_NAME
):
    return models.ForeignKey(
        model,
        verbose_name=pgettext_lazy('pxd_lingua', 'Translation entity'),
        null=False, blank=False, on_delete=models.CASCADE,
        related_name=related_name
    )


def create_simple_translation_model(
    model: models.Model,
    default_language: Optional[str] = EMPTY,
    languages: Optional[Sequence] = EMPTY,
    related_name: str = TRANSLATION_RELATED_NAME
):
    class TranslationModel(base_translated_model()):
        class Meta:
            abstract = True

        language = create_language_field(
            default_language=default_language,
            languages=languages
        )
        entity = create_entity_field(model, related_name=related_name)

    return TranslationModel


def create_translation_model(
    model: models.Model,
    fields: Optional[Sequence[str]] = None,
    postfix: str = TRANSLATION_POSTFIX,
    default_language: Optional[str] = EMPTY,
    languages: Optional[Sequence] = EMPTY,
    related_name: str = TRANSLATION_RELATED_NAME,
    stored_related_name: str = MAGIC_TRANSLATION_STORED_FIELD,
    language_control_related_name: str = MAGIC_TRANSLATION_CONTROL_FIELD,
    verbose_name: Optional[str] = None,
    verbose_name_plural: Optional[str] = None,
    abstract: bool = False,
    with_magic: bool = True,
) -> models.Model:
    base_name = model.__name__
    name = base_name + postfix
    no_fields = fields is None or len(fields) == 0

    assert not (not abstract and no_fields), (
        'Provide at least one field in `fields` or made model an abstract.'
    )

    Meta = type('Meta', (), {
        key: value
        for key, value in (
            ('verbose_name', verbose_name),
            ('verbose_name_plural', verbose_name_plural),
            ('abstract', abstract),
            ('base_manager_name', 'objects'),
            ('unique_together', translated_model_uniques()),
        )
        if value
    })

    TranslationModel = create_simple_translation_model(
        model, default_language=default_language, languages=languages,
        related_name=related_name
    )

    if with_magic:
        TranslationModel = apply_magic_to_translation_model(
            TranslationModel, model,
            entity_field=MAGIC_TRANSLATION_ENTITY_FIELD,
            stored_field=stored_related_name,
            control_field=language_control_related_name,
        )

    return type(name, (TranslationModel,), {
        **({} if no_fields else collect_model_fields(model, fields)),
        '__module__': model.__module__,
        'Meta': Meta,
    })


# For backward compatibility:
create_translated_model = create_translation_model
