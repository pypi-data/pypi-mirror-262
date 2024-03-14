from dataclasses import dataclass
from django.test import override_settings
from px_settings.contrib.django import settings


def test_simple_settings():
    with override_settings(CUSTOM_SETTINGS={'OTHER': 30}):
        @settings('CUSTOM_SETTINGS', { 'VALUE': 'base' })
        @dataclass
        class Settings:
            VALUE: str = 'initial'
            OTHER: int = 5

        first = Settings(OTHER=10)
        assert first.OTHER == 10
        assert first.VALUE == 'base'

        second = Settings(dict(VALUE='third'), dict(VALUE='second'))
        assert second.OTHER == 30
        assert second.VALUE == 'third'


@override_settings(
    CUSTOM_SETTINGS={
        'VALUE': 'base',
        'OTHER': 30
    },
    # This type of settings is more relevant, than object-defined
    CUSTOM_SETTINGS_OTHER='value'
)
def test_singular_resolver_settings():
    @settings('CUSTOM_SETTINGS')
    @dataclass
    class Settings:
        VALUE: str = 'initial'
        OTHER: int = 5

    first = Settings(OTHER=10)
    assert first.OTHER == 10
    assert first.VALUE == 'base'

    second = Settings(
        dict(VALUE='third'), dict(VALUE='second'), dict(not_existing=True)
    )
    assert second.OTHER == 'value'
    assert second.VALUE == 'third'
    assert hasattr(second, 'not_existing') is False


def test_settings_update():
    with override_settings(CUSTOM_SETTINGS={'OTHER': 30}):
        @settings('CUSTOM_SETTINGS')
        @dataclass
        class Settings:
            VALUE: str = 'initial'
            OTHER: int = 5

        first = Settings(OTHER=10)
        assert first.OTHER == 10
        assert first.VALUE == 'initial'

        with override_settings(CUSTOM_SETTINGS={'OTHER': 40, 'VALUE': 10}):
            first.update(VALUE='updated')
            assert first.OTHER == 40
            assert first.VALUE == 'updated'
