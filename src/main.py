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

    # Taste profile (upbeat-pop persona): target values for the features we score.
    user_prefs = {
        "target_genre": "pop",
        "target_energy": 0.75,
        "target_valence": 0.80,
        "target_danceability": 0.75,
        "target_tempo_bpm": 122,
    }

    print("\n" + "=" * 44)
    print("  USER TASTE PROFILE")
    print("=" * 44)
    for key, value in user_prefs.items():
        label = key.replace("target_", "").replace("_", " ").title()
        print(f"  {label:<14}: {value}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 44)
    print(f"  TOP {len(recommendations)} RECOMMENDATIONS")
    print("=" * 44)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Why:")
        for reason in explanation.split(", "):
            print(f"     • {reason}")

    print()


if __name__ == "__main__":
    main()
