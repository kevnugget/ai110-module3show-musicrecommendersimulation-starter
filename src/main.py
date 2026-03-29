"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    user_prefs = {
        "Late Night" : {
            "favorite_genre": "lofi",
            "favorite_mood": "focused",
            "target_energy": 0.40,
            "target_valence": 0.58,
            "likes_acoustic": True,
            }
        ,
        "Gym Session" : {
            "favorite_genre": "pop",
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "target_valence": 0.75,
            "likes_acoustic": False,
            }
        ,
        "Sunday Morning" : {
            "favorite_genre": "jazz",
            "favorite_mood": "relaxed",
            "target_energy": 0.35,
            "target_valence": 0.70,
            "likes_acoustic": True,
            }
        }

    # Switch between profiles here
    for preferences in user_prefs:
        user_prefs = user_prefs[preferences]
        recommendations = recommend_songs(user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
