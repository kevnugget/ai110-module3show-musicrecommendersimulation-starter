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
    user_one = {
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
    
    user_two = {
        "Road Trip" : {
            "favorite_genre": "rock",
            "favorite_mood": "energetic",
            "target_energy": 0.85,
            "target_valence": 0.60,
            "likes_acoustic": False,
        },
        "Study Time" : {
            "favorite_genre": "classical",
            "favorite_mood": "focused",
            "target_energy": 0.30,
            "target_valence": 0.50,
            "likes_acoustic": True,
        },
        "Party Vibes" : {
            "favorite_genre": "hip-hop",
            "favorite_mood": "upbeat",
            "target_energy": 0.90,
            "target_valence": 0.80,
            "likes_acoustic": False,
        }
    }
    users = [user_one, user_two]

    # Switch between profiles here
    for user in users:
        print(f"User Profile: {user}")
        for preferences in user:
            current_preferences = user[preferences]
            recommendations = recommend_songs(current_preferences, songs, k=3)
            print(f"\nRecommendations for {preferences}: {recommendations}\n")


if __name__ == "__main__":
    main()
