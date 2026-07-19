"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

# Moved output code to a smaller helper function to allow for different profiles to be passed through
def show_recommendations(name, prefs, songs, k=5):
    print("\n" + "=" * 44)
    print(f"  {name.upper()} — TASTE PROFILE")
    print("=" * 44)
    for key, value in prefs.items():
        label = key.replace("target_", "").replace("_", " ").title()
        print(f"  {label:<14}: {value}")

    recommendations = recommend_songs(prefs, songs, k=k)
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

def main() -> None:
    songs = load_songs("data/songs.csv") 

    '''
    # Default profile
    # Taste profile (upbeat-pop persona): target values for the features we score.
    user_prefs = {
        "target_genre": "pop",
        "target_energy": 0.75,
        "target_valence": 0.80,
        "target_danceability": 0.75,
        "target_tempo_bpm": 122,
    }
    '''


    rocky_heavy = {
        "target_genre": "rock",
        "target_energy": 0.90,
        "target_valence": 0.55,
        "target_danceability": 0.50,
        "target_tempo_bpm": 130,
    }

    not_technoblade = {
        "target_genre": "techno",
        "target_energy": 0.85,
        "target_valence": 0.80,
        "target_danceability": 0.85,
        "target_tempo_bpm": 150,    
    }

    hip_hopOptamus = {
        "target_genre": "hip hop",
        "target_energy": 0.70,
        "target_valence": 0.60,
        "target_danceability": 0.80,
        "target_tempo_bpm": 95,
    }

    # AI created System Evalauation user preferences:

    # test whether the algorithm degrades gracefully or produces nonsense "winner"
    emo_rager = {
    "target_genre": "metal",
    "target_energy": 0.95,        # wants it LOUD
    "target_valence": 0.05,       # ...but deeply sad
    "target_danceability": 0.10,  # ...and impossible to dance to
    "target_tempo_bpm": 60,       # ...yet very slow
    }
    
    # Numerically adversarial: chooses values outside of the ranges the math normally assumes
    out_of_bounds = {
    "target_genre": "polka",      # not in GENRE_FAMILIES → 0.0 for every song
    "target_energy": 1.5,         # >1 impossible
    "target_valence": -0.2,       # <0 impossible
    "target_danceability": 2.0,   # >1 impossible
    "target_tempo_bpm": 300,      # far outside the 60–168 range
    }

    # declare dictionary to iterate through each perference profile
    personas = {
        "Rock Heavy":      rocky_heavy,
        "Not Technoblade": not_technoblade,
        "Hip Hop-optamus": hip_hopOptamus,
        "Emo Rager":       emo_rager,
        "Out of Bounds":   out_of_bounds,
    }

    # Iterate through each profile and call helper function to output recommendations
    for name, pref in personas.items():
        show_recommendations(name, pref, songs)



if __name__ == "__main__":
    main()
