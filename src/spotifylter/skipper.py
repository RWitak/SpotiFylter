from multiprocessing.connection import Connection
from pprint import pprint
from typing import Callable, Optional

import requests.exceptions
import spotipy

from spotifylter.features import FEATURE_BOUNDS, FEATURE_NAMES
from spotifylter.time_util import now, now_plus, is_due


def print_track_info(current, feats) -> None:
    """
    Print info about a track to stdout.

    :param current:
    :param feats: A track's audio features.
    :return:
    """

    print("=================")
    print("Current Playback:")
    print("-----------------")

    for name in FEATURE_NAMES:
        if name in feats.keys():
            print(f"{name.replace('_', ' ').title()}: {round(feats[name], 2):.2f}")

    playback_string = f"{current['item']['artists'][0]['name']}: " \
                      f"{current['item']['name']}"

    print(len(playback_string) * "-")
    print(playback_string)
    print(len(playback_string) * "=")
    print()


def create_filter_funcs(feature_bounds: dict[str, tuple[float, float]]) -> set[Callable]:
    """
    Turns feature bounds into set of filter functions.

    :param feature_bounds: Upper and lower limits of audio features.
    :return: A set of lambda functions to validate a tracks features.
    """
    filters = set()

    if feature_bounds and FEATURE_BOUNDS != feature_bounds.values():
        filters.add(lambda feats: all([lower <= feats[feature] <= upper
                                       for feature, (lower, upper) in feature_bounds.items()]))

    return filters


def is_bad(feats, filter_funcs) -> bool:
    """
    Test if features meet all criteria.

    :param filter_funcs: A set of filter functions.
    :param feats: A set of audio features.
    :return: True if not all filter conditions are met, else False.
    """
    requirements = [filter_func(feats) for filter_func in filter_funcs]
    return not all(requirements)


class Skipper:
    """
    Class that handles live filtering of current Spotify playback.
    """
    client: spotipy.Spotify
    receiver: Optional[Connection]

    filter_funcs: set[Callable] = None
    current = None
    playing = True
    next_update = now()
    song_id = -1

    def __init__(self,
                 client: spotipy.Spotify,
                 feature_bounds: dict[str, tuple[float, float]] = None,
                 receiver: Connection = None):

        self.filter_funcs = create_filter_funcs(feature_bounds)
        self.client = client
        self.receiver = receiver

    def control_playback(self, ignore_current_song: bool = True):
        """
        Handles playback or lack thereof.

        :param ignore_current_song: If set to True, the current song will continue regardless of filters.
        :return: None
        """
        try:
            self.current = self.client.currently_playing()

            if not self.current or not self.current["is_playing"]:
                self.handle_no_playback()
                return

            current_song_id = self.current["item"]["id"]

            if ignore_current_song and current_song_id == self.song_id:
                time_to_next = self.current['item']['duration_ms'] - self.current['progress_ms']
                self.next_update = now_plus(ms=min(2000, time_to_next + 10))
                return
            else:
                self.song_id = current_song_id
                self.skip_if_unwanted()
                # self._unwanted_in_playlist()

        except requests.exceptions.ReadTimeout as error:
            self.next_update = now_plus(s=2)
            print(error)

    def handle_no_playback(self) -> None:
        """
        Prints message when missing playback is first noticed, and delays next update.
        Doesn't repeat until playback has resumed and stopped again.

        :return: None
        """
        if self.playing:
            print("=============================")
            print("No running playback detected.")
            print("=============================")
            print()
            self.playing = False
        self.next_update = now_plus(s=1)

    def skip_if_unwanted(self) -> None:
        """
        Gets current features and sends them for a check.
        Skips if track doesn't match current criteria.

        :return: None
        """
        feats = self.client.audio_features(self.song_id)[0]
        print_track_info(self.current, feats)
        if is_bad(feats, self.filter_funcs):
            self.client.next_track()

    def _unwanted_in_playlist(self, verbose=False) -> list[int]:
        """
        Analyzes the whole "context" of the current playback for matching criteria.
        Optionally prints short stats.

        :param verbose: Print number of bad tracks. (Default: False)
        :return: A list of tracks (via their IDs) that don't fit.
        """
        context = self.current['context']

        if not context:
            print("Can't fetch unwanted tracks outside of a playlist context!")
            return []

        tracks = self.get_tracks_from_context(context)

        bad_tracks = []
        good_tracks = []

        all_feats = self.client.audio_features(tracks)
        for feats, track in zip(all_feats, tracks):
            if is_bad(feats, self.filter_funcs):
                bad_tracks.append(track)
            else:
                good_tracks.append(track)

        if verbose:
            print(f"good_tracks: {len(good_tracks)}")
            print(f"bad_tracks: {len(bad_tracks)}")

        return bad_tracks

    def get_tracks_from_context(self, context) -> list[int]:
        """
        Tries to extract the tracks of a given context, independent of context type.

        :param context: Supported types: "playlist", "album".
        All others return list with single current track.

        :return: A list of all acquired tracks (by ID).
        """
        if context['type'] == 'playlist':
            items = self.client.playlist_items(context['uri'],
                                               additional_types=('track',)
                                               )["items"]
            tracks = [item['track']['id'] for item in items]
        elif context['type'] == 'album':
            items = self.client.album_tracks(context['uri'])
            tracks = items['items']
        else:
            tracks = [self.client.current_playback()['item']['uri']]
        return tracks

    def loop(self) -> None:
        """
        The main loop, waiting for either a feature bound update via Pipe
        or the expiration of an internal waiting period.

        :return: None
        """
        while True:
            if self.receiver and self.receiver.poll(timeout=0.05):
                self._handle_new_bounds()
                self.control_playback(ignore_current_song=False)
                continue

            if is_due(self.next_update):
                self.control_playback()

    def _handle_new_bounds(self) -> None:
        """
        Cleans the Pipe to get latest feature bounds submitted by GUI,
        prints the new values to stdout and calls method to update filters.

        :return: None
        """
        received = self.receiver.recv()

        while self.receiver.poll(timeout=0.05):
            received = self.receiver.recv()

        print("\nNEW BOUNDS:")
        pprint(received)
        print()

        self.filter_funcs = create_filter_funcs(received)
