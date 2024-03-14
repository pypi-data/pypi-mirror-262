import pytest

from datetime import datetime
from django.utils import timezone

from tests.testproject.models import Content, ContentTranslation


@pytest.mark.django_db
def test_translation_creation():
    instance = Content.objects.create(
        title='First',
        content='Content',
        published_at=timezone.now(),
    )

    assert instance.translations.count() == 0

    instance.translations.add(
        ContentTranslation(
            title='F First',
            content='F Content',
            published_at=timezone.now(),
            language='fr',
        ),
        ContentTranslation(
            title='D First',
            content='D Content',
            published_at=timezone.now(),
            language='de',
        ),
        ContentTranslation(
            title='E First',
            content='E Content',
            published_at=timezone.now(),
            language='en',
        ),
        bulk=False
    )

    assert instance.translations.count() == 3
    assert instance.translations.filter(language__in=('en', 'fr')).count() == 2
