from pprint import pprint
from time import sleep
from typing import Callable

import requests.exceptions
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from spotifylter.features import FEATURE_BOUNDS


class Skipper:
    client: spotipy.Spotify
    filter_funcs: set[Callable] = None
    current = None
    pause = 0
    filters_changed = False
    new_bounds = None
    song_id = -1

    def __init__(self, client, feature_bounds: dict[str, tuple[float, float]] = None):
        self.filter_funcs = create_filter_funcs(feature_bounds)
        self.client = client
        self.current = None

    def skip_unwanted(self):

        try:
            self.current = self.client.currently_playing()

            if not self.current or not self.current["is_playing"]:
                sleep(2)  # FIXME
                return

            current_song_id = self.current["item"]["id"]

            if current_song_id == self.song_id:
                time_to_next = self.current['item']['duration_ms'] - self.current['progress_ms']
                sleep(min(2, time_to_next / 1000 + 10))  # FIXME
                return
            else:
                self.song_id = current_song_id

                feats = self.client.audio_features(self.song_id)[0]
                pprint(feats)
                print()
                print(f"{self.current['item']['artists'][0]['name']}: {self.current['item']['name']}")
                print()

                if self._is_bad(feats):
                    self.client.next_track()

                self._unwanted_in_playlist()

        except requests.exceptions.ReadTimeout as error:
            sleep(10)  # FIXME
            print(error)

    def _unwanted_in_playlist(self) -> list[int]:
        context = self.current['context']

        if not context:
            print("Can't fetch unwanted tracks outside of a playlist context!")
            return []

        items = self.client.playlist_items(self.current['context']['uri'],
                                           additional_types=('track',)
                                           )["items"]

        bad_tracks = []
        good_tracks = []
        tracks = tuple(item['track']['id'] for item in items)

        all_feats = self.client.audio_features(tracks)
        for feats, track in zip(all_feats, tracks):
            if self._is_bad(feats):
                bad_tracks.append(track)
            else:
                good_tracks.append(track)

        print(f"good_tracks: {len(good_tracks)}")
        print(f"bad_tracks: {len(bad_tracks)}")

        return bad_tracks

    def _is_bad(self, feats):
        requirements = [filter_func(feats) for filter_func in self.filter_funcs]
        return not all(requirements)

    def update_bounds(self, feature_bounds: dict[str, tuple[float, float]]):
        self.filter_funcs = create_filter_funcs(feature_bounds)

    def loop(self):
        while True:
            if self.filters_changed:
                self.update_bounds(self.new_bounds)
                self.filters_changed = False

            if self.pause == 0:
                self.skip_unwanted()


def get_client() -> spotipy.Spotify:
    load_dotenv()
    scope = ["user-read-playback-state", "user-modify-playback-state"]
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def create_filter_funcs(feature_bounds: dict[str, tuple[float, float]]) -> set[Callable]:
    filters = set()

    for feature, (lower, upper) in feature_bounds.items():
        if FEATURE_BOUNDS[feature] != (lower, upper):
            filters.add(lambda feats: lower <= feats[feature] <= upper)

    return filters


if __name__ == '__main__':
    spotipy_client = get_client()
    skipper = Skipper(spotipy_client, {"valence": (0.3, 0.7),
                                       "energy": (0.1, 0.5),
                                       "instrumentalness": (0.3, 1.0)})
    skipper.loop()

# bad_tracks = unwanted_in_playlist(current, filter_funcs, sp)
# pprint(bad_tracks) if bad_tracks else True
