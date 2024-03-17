"""
Concrete :class:`~.base.TrackerJobsBase` subclass for ANT
"""

import functools

from ... import jobs, utils
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class AntTrackerJobs(TrackerJobsBase):

    @functools.cached_property
    def jobs_before_upload(self):
        return (
            # Interactive jobs
            self.tmdb_job,
            self.scene_check_job,

            # Background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.flags_job,
        )

    @functools.cached_property
    def flags_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('flags'),
            label='Flags',
            precondition=self.make_precondition('flags_job'),
            worker=self.autodetect_flags,
            no_output_is_ok=True,
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_flags(self, job):
        # supported flags: Directors, Extended, Uncut, IMAX, Unrated, HDR10, DV,
        # 4KRemaster, Atmos, DualAudio, Commentary, Remux, 3D, Criterion

        flags = []
        rn = self.release_name

        if "Director's Cut" in rn.edition:
            flags.append('Directors')
        if 'Extended Cut' in rn.edition:
            flags.append('Extended')
        if 'Uncut' in rn.edition:
            flags.append('Uncut')
        if 'Unrated' in rn.edition:
            flags.append('Unrated')
        if 'Criterion Collection' in rn.edition:
            flags.append('Criterion')
        if 'IMAX' in rn.edition:
            flags.append('IMAX')
        if '4k Remastered' in rn.edition:
            flags.append('4KRemaster')
        if 'Dual Audio' in rn.edition:
            flags.append('DualAudio')

        if 'Remux' in rn.source:
            flags.append('Remux')

        hdr_formats = utils.video.hdr_formats(self.content_path)
        if 'DV' in hdr_formats:
            flags.append('DV')
        if 'HDR10' in hdr_formats or 'HDR10+' in hdr_formats:
            flags.append('HDR10')

        if 'Atmos' in rn.audio_format:
            flags.append('Atmos')

        if utils.video.has_commentary(self.content_path):
            flags.append('Commentary')

        return flags

    @property
    def post_data(self):
        return {
            'api_key': self._tracker.apikey,
            'action': 'upload',
            'tmdbid': self.get_job_output(self.tmdb_job, slice=0).replace('movie/', ''),
            'mediainfo': self.get_job_output(self.mediainfo_job, slice=0),
            'flags[]': self.get_job_output(self.flags_job),
        }

    @property
    def post_files(self):
        return {
            'file_input': {
                'file': self.torrent_filepath,
                'mimetype': 'application/x-bittorrent',
            },
        }
