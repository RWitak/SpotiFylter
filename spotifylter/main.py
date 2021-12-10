from pprint import pprint
from time import sleep
from typing import Callable, Any, Union

import requests.exceptions
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class VocalSkipper:
    client: spotipy.Spotify
    filter_funcs: dict[str, Callable[[Any], Union[bool, Any]]] = None
    current = None

    def __init__(self, client, filter_funcs=None):
        self.filter_funcs = filter_funcs if filter_funcs else {}
        self.client = client
        self.current = None

    def skip_unwanted(self):
        song_id = -1

        while True:
            try:
                self.current = self.client.currently_playing()

                if not self.current["is_playing"]:
                    sleep(2)
                    continue

                current_song_id = self.current["item"]["id"]

                if current_song_id == song_id:
                    time_to_next = self.current['item']['duration_ms'] - self.current['progress_ms']
                    sleep(min(2, time_to_next / 1000 + 10))
                    continue
                else:
                    song_id = current_song_id

                    features = self.client.audio_features(song_id)[0]
                    pprint(features)
                    print()
                    print(f"{self.current['item']['artists'][0]['name']}: {self.current['item']['name']}")
                    print()

                    if self._is_bad(features):
                        self.client.next_track()

                    self._unwanted_in_playlist()

            except requests.exceptions.ReadTimeout:
                sleep(10)
                continue

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
        tracks = (item['track']['id'] for item in items)

        # FIXME: get all tracks at once with audio_features(tracks)
        for track in tracks:
            features = self.client.audio_features(track)[0]
            if self._is_bad(features):
                bad_tracks.append(track)
            else:
                good_tracks.append(track)

        print(f"good_tracks: {len(good_tracks)}")
        print(f"bad_tracks: {len(bad_tracks)}")

        return bad_tracks

    def _is_bad(self, features):
        red_flags = [fltr(features) for fltr in self.filter_funcs.values()]
        return any(red_flags)


if __name__ == '__main__':
    load_dotenv()
    scope = ["user-read-playback-state", "user-modify-playback-state"]

    filter_funcs = {
        "No singing": lambda feat:        feat['instrumentalness'] < 0.45,
        # "No live tracks": lambda feat:    feat['liveness'] < 0.5,
        # "No adrenaline": lambda feat:     feat['energy'] < 0.3,
        # "No dancing": lambda feat:        feat['danceability'] > 0.5,
        # "No downers": lambda feat:        feat['valence'] < 0.5,
        # "No smiling": lambda feat:        feat['valence'] > 0.3,
        # "No sitting around": lambda feat: feat['danceability'] < 0.5,
    }

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    skipper = VocalSkipper(sp, filter_funcs)
    skipper.skip_unwanted()

# bad_tracks = unwanted_in_playlist(current, filter_funcs, sp)
# pprint(bad_tracks) if bad_tracks else True
