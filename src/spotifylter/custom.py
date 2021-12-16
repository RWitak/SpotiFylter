CUSTOM_BOUNDS = {
    "acousticness":     (0.00, 1.00),
    "danceability":     (0.00, 1.00),
    "energy":           (0.00, 1.00),
    "instrumentalness": (0.00, 1.00),
    "liveness":         (0.00, 1.00),
    "speechiness":      (0.00, 1.00),
    "valence":          (0.00, 1.00)
}

"""
vvvvvvvvvvv
HOW TO USE:
^^^^^^^^^^^
* Set values above to desired levels.
* DO NOT CHANGE ANYTHING EXCEPT NUMBERS!
* Don't forget to enter values with decimal dot,
  not comma (so "0.75" instead of "0,75")! 
* Higher value means higher probability.
* "valence" is being happy/positive.
"""

if __name__ == '__main__':
    from spotifylter.main import run_headless
    run_headless(CUSTOM_BOUNDS)
