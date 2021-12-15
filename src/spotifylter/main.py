import os
from multiprocessing import Pipe, Process

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from spotifylter.front_end.gui import start_gui
from spotifylter.skipper import Skipper

ENV_VARS = ("SPOTIPY_CLIENT_ID",
            "SPOTIPY_CLIENT_SECRET")
SCOPE = ["user-read-playback-state", "user-modify-playback-state"]
REDIRECT_URI = "http://localhost:2340"


def incomplete_environment() -> bool:
    return not all(os.environ.get(var) for var in ENV_VARS)


def create_environment() -> None:
    load_dotenv()

    if incomplete_environment():
        with open(".env", 'a') as dot_env_file:
            for var in ENV_VARS:
                value = input(var + ": ")
                dot_env_file.write(f"{var}:{value}\n")

        load_dotenv(".env")


def get_client() -> spotipy.Spotify:
    create_environment()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE,
                                                     redirect_uri=REDIRECT_URI))


def run_headless() -> None:
    spotipy_client = get_client()
    skipper = Skipper(spotipy_client, {"valence": (0.3, 0.7),
                                       "energy": (0.1, 0.5),
                                       "instrumentalness": (0.3, 1.0)})
    skipper.loop()


def run_with_gui() -> None:
    # log_to_stderr(logging.INFO)

    receiver, sender = Pipe(duplex=False)

    front_end = Process(name="Front-End", target=start_gui, args=(sender,))
    front_end.start()

    spotipy_client = get_client()
    skipper = Skipper(spotipy_client, receiver=receiver)
    back_end = Process(name="Back-End", target=skipper.loop, daemon=True)
    back_end.start()

    front_end.join()


if __name__ == '__main__':
    run_headless()
