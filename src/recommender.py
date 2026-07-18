import csv
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
        """Stores the catalog of songs this recommender ranks over."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs best matching the given user's taste."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable reason why a song was recommended to a user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")

    numeric_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = dict(row)
            song["id"] = int(song["id"])
            for field in numeric_fields:
                song[field] = float(song[field])
            songs.append(song)

    return songs

# --- Genre families (fixes the categorical "cliff": exact 1.0, same family 0.5, else 0.0) ---
GENRE_FAMILIES = {
    "pop":        ["pop", "indie pop", "dream pop"],
    "rock":       ["rock", "metal"],
    "electronic": ["edm", "techno", "synthwave"],
    "chill":      ["lofi", "ambient"],
    "acoustic":   ["folk", "jazz", "classical", "country"],
    "urban":      ["hip hop", "r&b", "reggae"],
}
GENRE_TO_FAMILY = {g: fam for fam, gs in GENRE_FAMILIES.items() for g in gs}

# tempo_bpm is raw BPM (~60–168); normalize by this range so it doesn't dominate.
TEMPO_RANGE = 108.0


def genre_score(target_genre: str, song_genre: str) -> float:
    """
    Scores how well a song's genre matches the user's target genre.

    Returns 1.0 for an exact match, 0.5 when both genres belong to the same
    family (see GENRE_FAMILIES), and 0.0 otherwise. Softens the categorical
    "cliff" so adjacent genres still earn partial credit.
    """
    if song_genre == target_genre:
        return 1.0
    if GENRE_TO_FAMILY.get(song_genre) == GENRE_TO_FAMILY.get(target_genre):
        return 0.5
    return 0.0


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Per-feature rule: score = weight * (1 - distance), where distance is the
    absolute gap between the song's value and the user's target (tempo is
    normalized by TEMPO_RANGE first). Rewards nearness to the target.
    A perfect song totals 4.5.

    Returns (score, reasons) where reasons explains each point contribution.
    """
    score = 0.0
    reasons: List[str] = []

    # --- genre: direct point lookup (exact +1.0, same family +0.5, else 0) ---
    g = genre_score(user_prefs["target_genre"], song["genre"])
    if g > 0:
        score += g
        if g == 1.0:
            reasons.append(f"genre match: {song['genre']} (+{g:.1f})")
        else:
            reasons.append(f"same genre family as {user_prefs['target_genre']} (+{g:.1f})")

    # --- numeric features: weight * (1 - distance) ---
    # (feature key, target key, weight, distance normalizer)
    numeric_features = [
        ("energy",       "target_energy",       1.5, 1.0),
        ("valence",      "target_valence",      1.0, 1.0),
        ("danceability", "target_danceability", 0.5, 1.0),
        ("tempo_bpm",    "target_tempo_bpm",    0.5, TEMPO_RANGE),
    ]

    for feature, target_key, weight, normalizer in numeric_features:
        distance = abs(song[feature] - user_prefs[target_key]) / normalizer
        points = weight * (1 - distance)
        score += points
        reasons.append(f"{feature} near target (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Score every song, then keep the k highest — sorted highest to lowest.
    scored = [
        (song, *score_song(user_prefs, song))  # -> (song, score, reasons)
        for song in songs
    ]
    scored.sort(key=lambda item: item[1], reverse=True)

    return [
        (song, score, ", ".join(reasons))
        for song, score, reasons in scored[:k]
    ]
