"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs
from tabulate import tabulate
import re

# Friendly, word-based labels for each generated numeric reason.
# (mood and acousticness are intentionally absent — the scorer doesn't use them.)
REASON_LABELS = {
    "energy": "energy fit",
    "valence": "valence fit",
    "danceability": "danceability fit",
    "tempo_bpm": "tempo fit",
}


def top_reasons(explanation, n=3):
    """
    Summarize a generated explanation into its n highest-scoring reasons, in words.

    Each reason string ends with its point contribution, e.g. "energy near target
    (+1.46)". We parse those points, keep the n biggest, and phrase them as plain
    words (strongest first) so the "why" is readable instead of a wall of numbers.
    """
    parsed = []
    for reason in explanation.split(", "):
        match = re.search(r"\(\+?(-?\d+(?:\.\d+)?)\)\s*$", reason)
        points = float(match.group(1)) if match else 0.0
        if reason.startswith("genre match"):
            label = "exact genre match"
        elif reason.startswith("same genre family"):
            label = "same-genre family"
        else:
            key = reason.split(" ", 1)[0]
            label = REASON_LABELS.get(key, key)
        parsed.append((points, label))

    parsed.sort(key=lambda item: item[0], reverse=True)
    return ", ".join(label for _, label in parsed[:n])


# Moved output code to a smaller helper function to allow for different profiles to be passed through
def show_recommendations(name, prefs, songs, k=5):
    # --- Taste profile: two-column table of the user's target values ---
    print(f"\n{name.upper()} — TASTE PROFILE")
    profile_rows = [
        (key.replace("target_", "").replace("_", " ").title(), value)
        for key, value in prefs.items()
    ]
    print(tabulate(profile_rows, headers=["Attribute", "Value"], tablefmt="rounded_outline"))

    # --- Recommendations: one row per song; "Why" gives the top 3 reasons in words ---
    recommendations = recommend_songs(prefs, songs, k=k)
    print(f"\nTOP {len(recommendations)} RECOMMENDATIONS")
    table_rows = [
        [rank, song["title"], song["artist"], f"{score:.2f}", top_reasons(explanation)]
        for rank, (song, score, explanation) in enumerate(recommendations, start=1)
    ]
    print(tabulate(
        table_rows,
        headers=["#", "Title", "Artist", "Score", "Why (top 3 reasons)"],
        tablefmt="grid",
    ))
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
