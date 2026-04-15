from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class Song:
    """Represents a song and its audio features."""
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
    """Stores a user's music taste preferences for scoring comparisons."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool = False

class Recommender:
    """Scores and ranks songs against a UserProfile using weighted feature matching."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, str]:
        """Applies the scoring recipe to a single Song and returns (score, explanation)."""
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_sim = 1.0 - abs(song.energy - user.target_energy)
        score += energy_sim
        reasons.append(f"energy similarity +{energy_sim:.2f}")

        return score, ", ".join(reasons)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs sorted by score descending."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a plain-language explanation of why a song was recommended."""
        _, explanation = self._score(user, song)
        return explanation


def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of dicts with numeric fields cast to float."""
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """
    Scores a single song dict against user preference dict.

    Rules:
      +2.0  genre match
      +1.0  mood match
      +0-1  energy similarity = 1 - |song_energy - target_energy|

    Returns (score, explanation_string).
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_sim = 1.0 - abs(song["energy"] - user_prefs.get("energy", 0.5))
    score += energy_sim
    reasons.append(f"energy similarity +{energy_sim:.2f}")

    return score, ", ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts by score descending, and returns the top k as (song, score, explanation)."""
    scored = [(song, *score_song(song, user_prefs)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
