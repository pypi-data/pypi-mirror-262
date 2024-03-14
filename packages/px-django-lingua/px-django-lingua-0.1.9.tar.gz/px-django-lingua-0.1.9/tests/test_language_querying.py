import pytest
from itertools import groupby
from django.utils import timezone

from django.db import models
from django.utils.translation import override

from tests.testproject.models import Content, ContentTranslation


SECOND_TITLE = 'Second'


@pytest.fixture
def translations_data():
    titles = 'First', SECOND_TITLE, 'Third', 'Fourth', 'Fifth'
    languages = 'en', 'fr', 'de'

    for title in titles:
        instance = Content.objects.create(
            title=title,
            content='Content',
            published_at=timezone.now(),
        )

        instance.translations.add(
            *(
                ContentTranslation(
                    title=language + instance.title,
                    content=language + instance.content,
                    published_at=instance.published_at,
                    language=language,
                )
                for language in languages
            ),
            bulk=False
        )


@pytest.fixture
def translations_data_with_misses(translations_data):
    # Deleting French translation for a second title:
    count, _ = ContentTranslation.objects.filter(
        entity__title=SECOND_TITLE, language='fr'
    ).delete()

    assert count == 1


def ln(*langs):
    return ContentTranslation.objects.by_language_order(*langs)


@pytest.mark.django_db
def test_translations_language_fallback(
    translations_data
):
    assert ContentTranslation.objects.count() == 15

    assert ln('en', 'fr').count() == 5
    assert ln('en', 'fr').first().language == 'en'
    assert ln('fr', 'en').count() == 5
    assert ln('fr', 'en').first().language == 'fr'
    assert ln('en').count() == 5


@pytest.mark.django_db
def test_translations_language_fallback_with_misses(
    translations_data_with_misses
):
    # Checking the language ordering for previously cleaned entity:
    q = ln('fr', 'en')
    assert q.count() == 5
    languages = {
        x: len(list(items))
        for x, items in groupby(sorted([x.language for x in q]))
    }
    assert languages['en'] == 1
    assert languages['fr'] == 4

    # Another check, but with more than one fallback language:
    q = ln('fr', 'de', 'en')
    assert q.count() == 5
    languages = {
        x: len(list(items))
        for x, items in groupby(sorted([x.language for x in q]))
    }
    assert 'en' not in languages
    assert languages['de'] == 1
    assert languages['fr'] == 4

    assert ln('fr').count() == 4


@pytest.mark.django_db
def test_translations_related_manager_checks(
    translations_data_with_misses
):
    content = Content.objects.filter(title=SECOND_TITLE).first()
    translations = list(content.translations.by_language_order('fr', 'en'))

    assert len(translations) == 1
    assert translations[0].language == 'en'

    content = Content.objects.filter(title=SECOND_TITLE).first()
    translations = list(content.translations.by_language('en'))

    assert len(translations) == 1
    assert translations[0].language == 'en'


@pytest.mark.django_db
def test_translations_magic_querying_check(
    translations_data_with_misses, django_assert_num_queries
):
    content = Content.objects.filter(title=SECOND_TITLE).first()

    with override('en'):
        assert content.translated.language == 'en'
        assert content.translated.entity_id == content.id

    with override('fr'):
        # There should not be any updates here.
        # Because translated field will be resolved only once.
        assert content.translated.language == 'en'

    with django_assert_num_queries(1):
        content.language.inject('fr')
        assert content.translated == content

    with django_assert_num_queries(1):
        content.language.inject('de')
        assert content.translated.language == 'de'

    with django_assert_num_queries(0):
        content.language.inject('en')
        assert content.translated.language == 'en'

    with override('en'):
        content = Content.objects.filter(title=SECOND_TITLE).first()

        with django_assert_num_queries(1):
            content.language.inject('en')
            assert content.translated.language == 'en'
            assert content.language == 'en'
            assert content.language == content.language
            assert content.language != content

    with override('fr'):
        content = Content.objects.filter(title=SECOND_TITLE).first()

        with django_assert_num_queries(1):
            # FIXME: There is an issue with resolvement without injecton.
            # If there is no translation avaiable content instance will be
            # placed inside of a `translated` field.
            # But as content itself do not have a language it's impossible
            # for a `language` controller to determine with which language
            # this content had been placed into a cache.
            # Should do something with this.
            assert content.translated.language == ''
            assert content.translated == content

    content = Content.objects.filter(title=SECOND_TITLE).first()

    with override('fr'):
        assert content.translated.language == ''
        assert content.translated == content

    with override('en'):
        content.language.inject()
        assert content.translated.language == 'en'
        assert content.translated.entity_id == content.id


@pytest.mark.django_db
def test_translations_magic_prefetch(
    translations_data_with_misses, django_assert_num_queries
):
    with override('en'):
        content = (
            Content.objects
            .filter(title=SECOND_TITLE)
            .prefetch_related('translated')
            .first()
        )

        with django_assert_num_queries(0):
            content.language.inject('en')
            assert content.translated.language == 'en'

    # Check when it receives language
    with override('en'):
        content = (
            Content.objects
            .filter(title=SECOND_TITLE)
            .prefetch_related('translated')
        )

    with override('de'):
        content = content.first()

        with django_assert_num_queries(0):
            content.language.inject('de')
            assert content.translated.language == 'de'

    # Custom prefetch will get the language on the creation time
    with override('en'):
        content = (
            Content.objects
            .filter(title=SECOND_TITLE)
            .prefetch_related(
                models.Prefetch(
                    'translated',
                    queryset=ContentTranslation.objects.by_language()
                )
            )
        )

    with override('de'):
        content = content.first()

        with django_assert_num_queries(0):
            content.language.inject('en')
            assert content.translated.language == 'en'
