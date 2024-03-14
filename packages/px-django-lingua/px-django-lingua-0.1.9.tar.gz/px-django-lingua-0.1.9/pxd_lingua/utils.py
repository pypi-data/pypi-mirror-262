from typing import Optional, Sequence, Tuple

from django.db import models
from django.utils.translation import get_language as django_get_language
from django.conf import settings as django_settings

from .conf import settings
from .types import FallbackLanguages, Language


__all__ = (
    'get_language_choices',
    'get_language',
    'get_fallback_languages',
    'is_translation',
    'LanguageGetterMixin',
)


def get_language_choices(
    languages: Optional[Sequence[str]] = None
) -> Sequence[Tuple[str, str]]:
    languages = set(languages if languages is not None else settings.LANGUAGES)

    return [
        choice
        for choice in django_settings.LANGUAGES
        if choice[0] in languages
    ]


def get_language() -> Language:
    language = django_get_language()

    if language is None:
        return settings.DEFAULT_LANGUAGE

    return language


def get_fallback_languages(
    language: Optional[str] = None,
    fallback_languages: Optional[FallbackLanguages] = None
) -> Tuple[str, Sequence[str]]:
    fallback_languages = (
        fallback_languages if fallback_languages is not None
        else settings.FALLBACK_LANGUAGES
    )
    language = language if language is not None else get_language()

    return language, fallback_languages.get(language) or []


def is_translation(instance: models.Model):
    # FIXME: There could be an instance with some relation to another
    # "entity". So this check should be improved to be more accurate.
    return (
        hasattr(instance, 'entity_id')
        and
        hasattr(instance, 'language')
        and
        isinstance(instance.language, str)
    )


class LanguageGetterMixin:
    def get_language(self):
        return get_language()
