import pytest

from upsies.trackers.ptp import metadata


def test_TrumpableReason_members():
    assert list(metadata.TrumpableReason) == [
        metadata.TrumpableReason.NO_ENGLISH_SUBTITLES,
        metadata.TrumpableReason.HARDCODED_SUBTITLES,
    ]


@pytest.mark.parametrize(
    argnames='reason, exp_value',
    argvalues=(
        (metadata.TrumpableReason.NO_ENGLISH_SUBTITLES, 14),
        (metadata.TrumpableReason.HARDCODED_SUBTITLES, 4),
    ),
    ids=lambda v: repr(v),
)
def test_TrumpableReason_value(reason, exp_value):
    assert reason.value == exp_value


@pytest.mark.parametrize(
    argnames='reason, string',
    argvalues=(
        (metadata.TrumpableReason.NO_ENGLISH_SUBTITLES, 'No English Subtitles'),
        (metadata.TrumpableReason.HARDCODED_SUBTITLES, 'Hardcoded Subtitles'),
    ),
    ids=lambda v: repr(v),
)
def test_TrumpableReason_string(reason, string):
    assert str(reason) == string
    assert type(reason).from_string(string) is reason


def test_ArtistImportance_members():
    assert list(metadata.ArtistImportance) == [
        metadata.ArtistImportance.ACTOR,
        metadata.ArtistImportance.DIRECTOR,
        metadata.ArtistImportance.WRITER,
        metadata.ArtistImportance.PRODUCER,
        metadata.ArtistImportance.COMPOSER,
        metadata.ArtistImportance.CINEMATOGRAPHER,
    ]


@pytest.mark.parametrize(
    argnames='importance, exp_value',
    argvalues=(
        (metadata.ArtistImportance.DIRECTOR, 1),
        (metadata.ArtistImportance.WRITER, 2),
        (metadata.ArtistImportance.PRODUCER, 3),
        (metadata.ArtistImportance.COMPOSER, 4),
        (metadata.ArtistImportance.ACTOR, 5),
        (metadata.ArtistImportance.CINEMATOGRAPHER, 6),
    ),
    ids=lambda v: repr(v),
)
def test_ArtistImportance_value(importance, exp_value):
    assert importance.value == exp_value


@pytest.mark.parametrize(
    argnames='importance, string',
    argvalues=(
        (metadata.ArtistImportance.DIRECTOR, 'Director'),
        (metadata.ArtistImportance.WRITER, 'Writer'),
        (metadata.ArtistImportance.PRODUCER, 'Producer'),
        (metadata.ArtistImportance.COMPOSER, 'Composer'),
        (metadata.ArtistImportance.ACTOR, 'Actor'),
        (metadata.ArtistImportance.CINEMATOGRAPHER, 'Cinematographer'),
    ),
    ids=lambda v: repr(v),
)
def test_ArtistImportance_string(importance, string):
    assert str(importance) == string
    assert type(importance).from_string(string) is importance
