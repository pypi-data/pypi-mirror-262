from unittest.mock import Mock, PropertyMock, call

import pytest

from upsies.trackers import ant


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.name = 'ant'
    return tracker


@pytest.fixture
def ant_tracker_jobs(tracker, tmp_path, mocker):
    content_path = tmp_path / 'Foo 2000 1080p BluRay x264-ASDF'

    ant_tracker_jobs = ant.AntTrackerJobs(
        content_path=str(content_path),
        tracker=tracker,
        image_hosts=(),
        btclient=Mock(),
        torrent_destination=str(tmp_path / 'destination'),
        common_job_args={
            'home_directory': str(tmp_path / 'home_directory'),
            'ignore_cache': True,
        },
        options=None,
    )

    return ant_tracker_jobs


@pytest.fixture
def mock_job_attributes(ant_tracker_jobs, mocker):
    job_attrs = (
        # Interactive jobs
        'tmdb_job',
        'scene_check_job',

        # Background jobs
        'create_torrent_job',
        'mediainfo_job',
        'flags_job',
    )
    for job_attr in job_attrs:
        mocker.patch.object(
            type(ant_tracker_jobs),
            job_attr,
            PropertyMock(return_value=Mock(attr=job_attr, prejobs=())),
        )


def test_jobs_before_upload_items(ant_tracker_jobs, mock_job_attributes, mocker):
    assert tuple(job.attr for job in ant_tracker_jobs.jobs_before_upload) == (
        # Interactive jobs
        'tmdb_job',
        'scene_check_job',

        # Background jobs
        'create_torrent_job',
        'mediainfo_job',
        'flags_job',
    )


def test_flags_job(ant_tracker_jobs, mocker):
    CustomJob_mock = mocker.patch('upsies.jobs.custom.CustomJob')
    mocker.patch.object(ant_tracker_jobs, 'get_job_name')
    mocker.patch.object(ant_tracker_jobs, 'make_precondition')
    mocker.patch.object(ant_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert ant_tracker_jobs.flags_job is CustomJob_mock.return_value
    assert CustomJob_mock.call_args_list == [call(
        name=ant_tracker_jobs.get_job_name.return_value,
        label='Flags',
        precondition=ant_tracker_jobs.make_precondition.return_value,
        worker=ant_tracker_jobs.autodetect_flags,
        no_output_is_ok=True,
        common_job_arg='common job argument',
    )]
    assert ant_tracker_jobs.get_job_name.call_args_list == [call('flags')]
    assert ant_tracker_jobs.make_precondition.call_args_list == [call('flags_job')]
    assert ant_tracker_jobs.common_job_args.call_args_list == [call(ignore_cache=True)]


@pytest.mark.parametrize(
    argnames='attrs, exp_flags',
    argvalues=(
        ({}, []),
        ({'edition': ["Director's Cut"]}, ['Directors']),
        ({'edition': ['Extended Cut']}, ['Extended']),
        ({'edition': ['Uncut']}, ['Uncut']),
        ({'edition': ['Unrated']}, ['Unrated']),
        ({'edition': ['Criterion Collection']}, ['Criterion']),
        ({'edition': ['IMAX']}, ['IMAX']),
        ({'edition': ['4k Remastered']}, ['4KRemaster']),
        ({'edition': ['Dual Audio']}, ['DualAudio']),
        ({'source': 'BluRay Remux'}, ['Remux']),
        ({'source': 'DVD Remux'}, ['Remux']),
        ({'hdr_formats': ('DV')}, ['DV']),
        ({'hdr_formats': ('HDR')}, []),
        ({'hdr_formats': ('HDR10')}, ['HDR10']),
        ({'hdr_formats': ('HDR10+')}, ['HDR10']),
        ({'audio_format': 'DDP Atmos'}, ['Atmos']),
        ({'has_commentary': False}, []),
        ({'has_commentary': True}, ['Commentary']),
        (
            {
                'edition': ["Director's Cut", 'Extended Cut', '4k Remastered'],
                'source': 'WEB-DL Remux',
                'hdr_formats': ('DV', 'HDR10+'),
                'audio_format': 'TrueHD Atmos',
                'has_commentary': True,
            },
            [
                "Directors", 'Extended', '4KRemaster',
                'Remux',
                'DV', 'HDR10',
                'Atmos',
                'Commentary',
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_autodetect_flags(attrs, exp_flags, ant_tracker_jobs, mocker):
    mocker.patch.object(type(ant_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        edition=attrs.get('edition', []),
        source=attrs.get('source', ''),
        audio_format=attrs.get('audio_format', ''),
    )))
    mocker.patch('upsies.utils.video.hdr_formats', return_value=attrs.get('hdr_formats', ()))
    mocker.patch('upsies.utils.video.has_commentary', return_value=attrs.get('has_commentary', False))

    return_value = await ant_tracker_jobs.autodetect_flags('job_')
    assert return_value == exp_flags


async def test_post_data(ant_tracker_jobs, mocker):
    mocker.patch.object(type(ant_tracker_jobs), 'tmdb_job', PropertyMock())
    mocker.patch.object(type(ant_tracker_jobs), 'mediainfo_job', PropertyMock())
    mocker.patch.object(type(ant_tracker_jobs), 'flags_job', PropertyMock())
    mocker.patch.object(ant_tracker_jobs, '_tracker', Mock(
        apikey='d34db33f',
    ))
    mocker.patch.object(ant_tracker_jobs, 'get_job_output', side_effect=(
        'movie/123456',
        '[mediainfo]',
        ('Uncut', 'Commentary'),
    ))

    assert ant_tracker_jobs.post_data == {
        'api_key': 'd34db33f',
        'action': 'upload',
        'tmdbid': '123456',
        'mediainfo': '[mediainfo]',
        'flags[]': ('Uncut', 'Commentary'),
    }
    assert ant_tracker_jobs.get_job_output.call_args_list == [
        call(ant_tracker_jobs.tmdb_job, slice=0),
        call(ant_tracker_jobs.mediainfo_job, slice=0),
        call(ant_tracker_jobs.flags_job),
    ]


async def test_post_files(ant_tracker_jobs, mocker):
    mocker.patch.object(type(ant_tracker_jobs), 'torrent_filepath', PropertyMock(
        return_value='path/to/torrent',
    ))

    assert ant_tracker_jobs.post_files == {
        'file_input': {
            'file': 'path/to/torrent',
            'mimetype': 'application/x-bittorrent',
        },
    }
