from dataclasses import dataclass
import pytest
import warnings
from px_settings import settings


class Success(Warning):
    pass


def test_simple_settings():
    @settings({ 'VALUE': 'base' })
    @dataclass
    class Settings:
        VALUE: str = 'initial'
        OTHER: int = 5

    first = Settings(OTHER=10)
    assert first.OTHER == 10
    assert first.VALUE == 'base'

    second = Settings(dict(VALUE='third'), dict(VALUE='second'))
    assert second.OTHER == 5
    assert second.VALUE == 'third'


def test_settings_update():
    @settings({ 'VALUE': 'base' })
    @dataclass
    class Settings:
        VALUE: str = 'initial'
        OTHER: int = 5

    first = Settings(OTHER=10)
    assert first.OTHER == 10
    assert first.VALUE == 'base'

    first.update(VALUE='updated')
    assert first.VALUE == 'updated'


def test_settings_update_warn():
    @settings({ 'update': 'base' })
    @dataclass
    class Settings:
        update: str = 'initial'

    with pytest.warns(ResourceWarning):
        first = Settings()
        assert first.update == 'base'

    @settings()
    @dataclass
    class Settings:
        update: str = 'initial'

    with pytest.warns(ResourceWarning):
        first = Settings()
        assert first.update == 'initial'

    @settings()
    @dataclass
    class Settings:
        updated: str = 'initial'

    with pytest.warns(Success) as record:
        first = Settings()
        assert first.updated == 'initial'

        if len(record) == 0:
            warnings.warn(Success())
