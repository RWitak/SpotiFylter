FEATURE_NAMES = ("acousticness",
                 "danceability",
                 "energy",
                 "instrumentalness",
                 # "key",
                 "liveness",
                 # "loudness",
                 # "mode",
                 "speechiness",
                 # "time_signature",
                 "valence")

FEATURE_BOUNDS = {"acousticness":     (0.0, 1.0),
                  "danceability":     (0.0, 1.0),
                  "energy":           (0.0, 1.0),
                  "instrumentalness": (0.0, 1.0),
                  # "key":            (-1, 11),  # -1 = not detected
                  "liveness":         (0.0, 1.0),
                  # "loudness":         (0.0, 1.0), TODO: use correct bounds, "typically between -60dB and 0dB"
                  # "mode":           (0, 1),  # 0 = minor, 1 = major
                  "speechiness":      (0.0, 1.0),
                  # "time_signature": (3, 7),  # quarters per bar
                  "valence":          (0.0, 1.0)}
