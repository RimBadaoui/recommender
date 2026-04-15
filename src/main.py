"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Prints a labeled block of top-k recommendations with scores and reasons."""
    print(f"\n{'='*55}")
    print(f"  Profile: {label}")
    print(f"  Prefs:   genre={user_prefs.get('genre')}, mood={user_prefs.get('mood')}, energy={user_prefs.get('energy')}")
    print(f"{'='*55}")
    results = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        (
            "High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.9},
        ),
        (
            "Chill Lofi",
            {"genre": "lofi", "mood": "chill", "energy": 0.35},
        ),
        (
            "Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.92},
        ),
        (
            "Edge Case — High Energy but Sad Mood",
            {"genre": "synthwave", "mood": "sad", "energy": 0.95},
        ),
    ]

    for label, prefs in profiles:
        print_recommendations(label, prefs, songs)


if __name__ == "__main__":
    main()
