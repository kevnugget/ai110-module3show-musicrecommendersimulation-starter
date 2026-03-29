from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


# --- Scoring weights ---
GENRE_WEIGHT    = 0.5   # Genre match: broadest filter, highest penalty for a miss
MOOD_WEIGHT     = 1.0   # Mood match: important but more flexible than genre
ENERGY_WEIGHT   = 1.0   # Energy proximity: most differentiating numerical feature
VALENCE_WEIGHT  = 0.5   # Valence proximity: tiebreaker nuance
ACOUSTIC_BONUS  = 0.5   # Bonus when user likes acoustic and song is highly acoustic

# Max possible score = 2.0 + 1.0 + 1.0 + 0.5 + 0.5 = 5.0


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """
    Scoring Rule: compute a compatibility score for one song against a user profile.
    Returns (score, explanation string).
    """
    score = 0.0
    reasons = []

    # Categorical: +GENRE_WEIGHT for an exact genre match
    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({song['genre']})")

    # Categorical: +MOOD_WEIGHT for an exact mood match
    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({song['mood']})")

    # Numerical proximity: rewards closeness to the user's target energy
    # Score = 1 - |song_value - user_target|, scaled by weight
    energy_proximity = 1 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_proximity * ENERGY_WEIGHT
    reasons.append(f"energy proximity {energy_proximity:.2f}")

    # Numerical proximity: valence closeness
    valence_proximity = 1 - abs(song["valence"] - user_prefs["target_valence"])
    score += valence_proximity * VALENCE_WEIGHT
    reasons.append(f"valence proximity {valence_proximity:.2f}")

    # Acoustic bonus: reward high-acousticness songs for users who prefer them
    if user_prefs.get("likes_acoustic") and song["acousticness"] >= 0.6:
        score += ACOUSTIC_BONUS
        reasons.append(f"acoustic bonus ({song['acousticness']})")

    explanation = ", ".join(reasons)
    return score, explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranking Rule: score every song and return the top-k using a min heap.

    A min heap of size k keeps only the k highest-scoring songs seen so far.
    For each song:
      - If the heap has fewer than k items, push unconditionally.
      - Otherwise, if this song scores higher than the current minimum (heap[0]),
        pop the minimum and push the new song.
    This runs in O(n log k) instead of O(n log n) for a full sort.

    Returns list of (song_dict, score, explanation) sorted best-first.
    """
    import heapq

    heap = []  # min heap of (score, index, song, explanation)
                # 'index' breaks score ties so Song dicts are never compared

    for i, song in enumerate(songs):
        score, explanation = score_song(song, user_prefs)

        if len(heap) < k:
            heapq.heappush(heap, (score, i, song, explanation))
        elif score > heap[0][0]:          # better than current worst in top-k
            heapq.heapreplace(heap, (score, i, song, explanation))

    # heap contains top-k entries; sort descending for final output
    top_k = sorted(heap, key=lambda x: x[0], reverse=True)
    return [(song, score, explanation) for score, _, song, explanation in top_k]
