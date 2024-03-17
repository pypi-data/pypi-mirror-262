import re
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import errors
from upsies.trackers.ant import AntTracker, AntTrackerConfig, AntTrackerJobs


@pytest.fixture
def make_tracker():
    def make_tracker(options={}):
        options_ = {
            'username': 'bunny',
            'password': 'hunter2',
            'base_url': 'http://ant.local',
        }
        options_.update(options)
        return AntTracker(options=options_)

    return make_tracker


@pytest.fixture
def tracker(make_tracker):
    return make_tracker()


def test_name_attribute():
    assert AntTracker.name == 'ant'


def test_label_attribute():
    assert AntTracker.label == 'ANT'


def test_TrackerConfig_attribute():
    assert AntTracker.TrackerConfig is AntTrackerConfig


def test_TrackerJobs_attribute():
    assert AntTracker.TrackerJobs is AntTrackerJobs


def test_base_url_attribute(make_tracker):
    tracker = make_tracker(options={'base_url': 'http://foo.local'})
    assert tracker._base_url == 'http://foo.local'


def test_api_url_attribute(make_tracker):
    tracker = make_tracker(options={'base_url': 'http://foo.local'})
    assert tracker._api_url == 'http://foo.local/api.php'


@pytest.mark.parametrize(
    argnames='options, exp_result',
    argvalues=(
        ({}, errors.RequestError('No API key configured')),
        ({'apikey': ''}, errors.RequestError('No API key configured')),
        ({'apikey': 'd34db33f'}, 'd34db33f'),
    ),
    ids=lambda v: repr(v),
)
def test_apikey_attribute(options, exp_result, make_tracker):
    tracker = make_tracker(options=options)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker.apikey
    else:
        assert tracker.apikey == exp_result


@pytest.mark.asyncio
async def test_login(tracker):
    return_value = await tracker._login()
    assert return_value is None


@pytest.mark.asyncio
async def test_logout(tracker):
    return_value = await tracker._logout()
    assert return_value is None


@pytest.mark.parametrize(
    argnames='options, exp_result',
    argvalues=(
        ({}, errors.AnnounceUrlNotSetError(tracker=Mock())),
        ({'announce_url': ''}, errors.AnnounceUrlNotSetError(tracker=Mock())),
        ({'announce_url': 'http://mock.tracker/annnounce'}, 'http://mock.tracker/annnounce'),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_announce_url(options, exp_result, make_tracker):
    tracker = make_tracker(options=options)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$') as exc_info:
            await tracker.get_announce_url()
        assert exc_info.value.tracker == tracker
    else:
        return_value = await tracker.get_announce_url()
        assert return_value == exp_result


@pytest.mark.parametrize(
    argnames='response, exp_result',
    argvalues=(
        (
            {'status': 'success'},
            '{torrent_filepath}',
        ),
        (
            {'error': 'Nope'},
            errors.RequestError('Upload failed: Nope'),
        ),
        (
            {'wat': 'dis'},
            RuntimeError("Unexpected response: {'wat': 'dis'}"),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_upload(response, exp_result, tracker, mocker):
    tracker_jobs = Mock(
        post_data={'foo': 'this', 'bar': 'that'},
        post_files={'my': 'files'},
        torrent_filepath='/path/to.torrent',
    )
    mocker.patch.object(tracker, '_request', return_value=response)

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await tracker.upload(tracker_jobs)
    else:
        return_value = await tracker.upload(tracker_jobs)
        assert return_value == exp_result.format(torrent_filepath=tracker_jobs.torrent_filepath)

    assert tracker._request.call_args_list == [call(
        method='POST',
        url=tracker._api_url,
        cache=False,
        data=tracker_jobs.post_data,
        files=tracker_jobs.post_files,
    )]


@pytest.mark.parametrize(
    argnames='response, exp_result',
    argvalues=(
        (
            Mock(json=Mock(return_value={'success': 'json'})),
            {'success': 'json'},
        ),
        (
            errors.RequestError('{"error": "json"}', text='{"error": "json"}'),
            {'error': 'json'},
        ),
        (
            errors.RequestError('This is not JSON.'),
            errors.RequestError('This is not JSON.'),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test__request(response, exp_result, tracker, mocker):
    method = 'GET_or_POST'
    http_mock = Mock()
    if isinstance(response, Exception):
        http_mock.get_or_post = AsyncMock(side_effect=response)
    else:
        http_mock.get_or_post = AsyncMock(return_value=response)

    args = ('foo', 'bar')
    kwargs = {'this': 'that'}

    mocker.patch('upsies.utils.http', http_mock, create=True)

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await tracker._request(method, *args, **kwargs)
    else:
        return_value = await tracker._request(method, *args, **kwargs)
        assert return_value == exp_result

    assert http_mock.get_or_post.call_args_list == [call(
        *args,
        user_agent=True,
        **kwargs,
    )]


@pytest.mark.parametrize(
    argnames='bytes, exp_piece_size',
    argvalues=(
        # ~1 - ~1000 MiB
        (1 * 2**20, 2**20),
        (10 * 2**20, 2**20),
        (100 * 2**20, 2**20),
        (1000 * 2**20, 2**20),

        # ~1 - ~10 GiB
        (1 * 2**30, 2 * 2**20),
        (3 * 2**30, 4 * 2**20),
        (6 * 2**30, 8 * 2**20),
        (9 * 2**30, 16 * 2**20),

        # ~10 - ~100 GiB
        (10 * 2**30, 16 * 2**20),
        (12 * 2**30, 16 * 2**20),
        (15 * 2**30, 16 * 2**20),
        (24 * 2**30, 32 * 2**20),
        (36 * 2**30, 64 * 2**20),
        (48 * 2**30, 64 * 2**20),
        (72 * 2**30, 64 * 2**20),
        (96 * 2**30, 64 * 2**20),

        # ~100 - ~1000 GiB
        (100 * 2**30, 64 * 2**20),
        (192 * 2**30, 64 * 2**20),
        (384 * 2**30, 64 * 2**20),
        (786 * 2**30, 64 * 2**20),
        (960 * 2**30, 64 * 2**20),
        (1000 * 2**30, 64 * 2**20),
    ),
)
def test_calculate_piece_size(bytes, exp_piece_size):
    piece_size = AntTracker.calculate_piece_size(bytes)
    assert piece_size == exp_piece_size


@pytest.mark.parametrize(
    argnames='bytes, exp_piece_size_min_max',
    argvalues=(
        # ~1 - ~1000 MiB
        (1 * 2**20, (1 * 2**20, 2**26)),
        (10 * 2**20, (1 * 2**20, 2**26)),
        (100 * 2**20, (1 * 2**20, 2**26)),
        (1000 * 2**20, (1 * 2**20, 2**26)),

        # ~1 - ~10 GiB
        (1 * 2**30, (1 * 2**20, 2**26)),
        (3 * 2**30, (1 * 2**20, 2**26)),
        (6 * 2**30, (2 * 2**20, 2**26)),
        (9 * 2**30, (4 * 2**20, 2**26)),

        # ~10 - ~100 GiB
        (10 * 2**30, (4 * 2**20, 2**26)),
        (12 * 2**30, (4 * 2**20, 2**26)),
        (15 * 2**30, (8 * 2**20, 2**26)),
        (24 * 2**30, (8 * 2**20, 2**26)),
        (36 * 2**30, (8 * 2**20, 2**26)),
        (48 * 2**30, (8 * 2**20, 2**26)),
        (72 * 2**30, (8 * 2**20, 2**26)),
        (96 * 2**30, (8 * 2**20, 2**26)),

        # ~100 - ~1000 GiB
        (100 * 2**30, (8 * 2**20, 2**26)),
        (192 * 2**30, (8 * 2**20, 2**26)),
        (384 * 2**30, (8 * 2**20, 2**26)),
        (786 * 2**30, (8 * 2**20, 2**26)),
        (960 * 2**30, (8 * 2**20, 2**26)),
        (1000 * 2**30, (8 * 2**20, 2**26)),
    ),
    ids=lambda v: repr(v),
)
def test_calculate_piece_size_min_max(bytes, exp_piece_size_min_max):
    piece_size_min_max = AntTracker.calculate_piece_size_min_max(bytes)
    assert piece_size_min_max == exp_piece_size_min_max
