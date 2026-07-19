# 🎵 Music Recommender Simulation

## Project Summary

DownloadDash is a small content-based recommender. It represents each song and a user "taste profile" as numeric features (energy, valence, danceability, tempo) plus a genre, scores every song by how closely it matches the profile and returns the top songs with a short explanation of why each was chosen. This project builds that scoring rule, evaluates it against several user profiles (including deliberately broken ones) and reflects on its biases in the the [**Model Card**](model_card.md)

---

## How The System Works

A real-world recommendation system works by blending several different methods:  filtering on listeners' behavior (listening history, skips, likes, etc.,), content based matching on audio traits (such as energy, tempo, etc.,) and collaborative filtering to further offer recommendations based on other users with similar likes/tastes. 

Using a pure content based matching system, we can then prioritize those attributes which contribute *more* to likeability and score them. Each song is scored by comparing its input data (features) to the user's target preferences. The closer a song's values are to what the user wants, the higher its score.
Then using those scores, we can rank the songs and be able to "hand back" a top 5 list to the user.
 

Since users mostly enjoy and want more of the music which resonates with them, focusing on those attributes will be the most helpful with recommending songs. Attributes such as song id, song name while they may contribute to a future song a user may like, attributes such as energy, danceability, or valence affect it more. 

For `Songs`, we'll be using:
* energy
* valence
* danceability
* tempo_bpm
* genre

For `UserProfile`, we'll be using:
* target_energy
* target_valence
* target_danceability
* target_tempo_bpm
* target_genre

### How the score is computed (algorithm recipe)

Each song earns points by how well it matches the profile (a perfect song totals 4.5):

| Feature | Rule | Max |
|---|---|---|
| genre | exact match +1.0, same family +0.5, else 0 | 1.0 |
| energy | 1.5 × (1 − distance) | 1.5 |
| valence | 1.0 × (1 − distance) | 1.0 |
| danceability | 0.5 × (1 − distance) | 0.5 |
| tempo_bpm | 0.5 × (1 − normalized distance) | 0.5 |

- **distance** = how far a song's value is from the user's target; closer = more points.
- **tempo** is normalized by the catalog's BPM range so it can't dominate the score.
- **Genre families** group similar genres (e.g. rock/metal), so a near-genre still earns partial credit.

Energy is the single heaviest lever (1.5 of 4.5); genre is kept intentionally light so a great song in a *different* genre can still be recommended, rather than being buried by a large genre penalty. Songs are then **ranked** by total score, and the **top 5** are returned.

### Potential biases

- **Energy bias:** because energy carries the most weight, the system may over-prioritize energy and rank an energetic-but-emotionally-mismatched song above one that better fits the user's mood. A high-energy song with the "wrong" feel can still score well.
- **Ignored dimensions:** `mood` and `acousticness` are not scored at all, so any taste tied to those traits is invisible to the recommender.
- **Subjective genre families:** the family groupings are hand-picked, so which genres count as "similar" reflects my own assumptions rather than any objective measure.
- **Small, uneven catalog:** with only a handful of songs and some genres better represented than others, well-covered genres (pop, lofi) have more chances to surface than sparse ones (classical, reggae).
- **Single-point profile:** one set of target values can't represent a listener who genuinely likes two very different styles at once (e.g. intense rock *and* chill lofi).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

**Initial Output using _default_ user profile**
```
============================================
  USER TASTE PROFILE
============================================
  Genre         : pop
  Energy        : 0.75
  Valence       : 0.8
  Danceability  : 0.75
  Tempo Bpm     : 122

============================================
  TOP 5 RECOMMENDATIONS
============================================

1. Sunrise City — Neon Echo
   Score: 4.32
   Why:
     • genre match: pop (+1.0)
     • energy near target (+1.40)
     • valence near target (+0.96)
     • danceability near target (+0.48)
     • tempo_bpm near target (+0.48)

2. Gym Hero — Max Pulse
   Score: 4.09
   Why:
     • genre match: pop (+1.0)
     • energy near target (+1.23)
     • valence near target (+0.97)
     • danceability near target (+0.43)
     • tempo_bpm near target (+0.45)

3. Rooftop Lights — Indigo Parade
   Score: 3.93
   Why:
     • same genre family as pop (+0.5)
     • energy near target (+1.48)
     • valence near target (+0.99)
     • danceability near target (+0.47)
     • tempo_bpm near target (+0.49)

4. Night Drive Loop — Neon Echo
   Score: 3.12
   Why:
     • energy near target (+1.50)
     • valence near target (+0.69)
     • danceability near target (+0.49)
     • tempo_bpm near target (+0.44)

5. Paper Boats — Little Harbor
   Score: 3.10
   Why:
     • same genre family as pop (+0.5)
     • energy near target (+0.99)
     • valence near target (+0.83)
     • danceability near target (+0.40)
     • tempo_bpm near target (+0.38)
```

**Now using 3 different profiles AND 2 AI generated _edge test_ profiles**
```
Loading songs from data/songs.csv...

============================================
  ROCK HEAVY — TASTE PROFILE
============================================
  Genre         : rock
  Energy        : 0.9
  Valence       : 0.55
  Danceability  : 0.5
  Tempo Bpm     : 130

============================================
  TOP 5 RECOMMENDATIONS
============================================

1. Storm Runner — Voltline
   Score: 4.23
   Why:
     • genre match: rock (+1.0)
     • energy near target (+1.48)
     • valence near target (+0.93)
     • danceability near target (+0.42)
     • tempo_bpm near target (+0.40)

2. Iron Verdict — Ashfall
   Score: 3.42
   Why:
     • same genre family as rock (+0.5)
     • energy near target (+1.40)
     • valence near target (+0.71)
     • danceability near target (+0.49)
     • tempo_bpm near target (+0.32)

3. Signal Lost — Grid Runner
   Score: 3.24
   Why:
     • energy near target (+1.47)
     • valence near target (+0.94)
     • danceability near target (+0.33)
     • tempo_bpm near target (+0.50)

4. Neon Alley — Pulse Theory
   Score: 3.04
   Why:
     • energy near target (+1.43)
     • valence near target (+0.83)
     • danceability near target (+0.29)
     • tempo_bpm near target (+0.49)

5. Gym Hero — Max Pulse
   Score: 3.04
   Why:
     • energy near target (+1.46)
     • valence near target (+0.78)
     • danceability near target (+0.31)
     • tempo_bpm near target (+0.49)


============================================
  NOT TECHNOBLADE — TASTE PROFILE
============================================
  Genre         : techno
  Energy        : 0.85
  Valence       : 0.8
  Danceability  : 0.85
  Tempo Bpm     : 150

============================================
  TOP 5 RECOMMENDATIONS
============================================

1. Signal Lost — Grid Runner
   Score: 4.05
   Why:
     • genre match: techno (+1.0)
     • energy near target (+1.46)
     • valence near target (+0.69)
     • danceability near target (+0.49)
     • tempo_bpm near target (+0.41)

2. Neon Alley — Pulse Theory
   Score: 3.64
   Why:
     • same genre family as techno (+0.5)
     • energy near target (+1.35)
     • valence near target (+0.92)
     • danceability near target (+0.47)
     • tempo_bpm near target (+0.40)

3. Night Drive Loop — Neon Echo
   Score: 3.29
   Why:
     • same genre family as techno (+0.5)
     • energy near target (+1.35)
     • valence near target (+0.69)
     • danceability near target (+0.44)
     • tempo_bpm near target (+0.31)

4. Gym Hero — Max Pulse
   Score: 3.25
   Why:
     • energy near target (+1.38)
     • valence near target (+0.97)
     • danceability near target (+0.48)
     • tempo_bpm near target (+0.42)

5. Sunrise City — Neon Echo
   Score: 3.24
   Why:
     • energy near target (+1.46)
     • valence near target (+0.96)
     • danceability near target (+0.47)
     • tempo_bpm near target (+0.35)


============================================
  HIP HOP-OPTAMUS — TASTE PROFILE
============================================
  Genre         : hip hop
  Energy        : 0.7
  Valence       : 0.6
  Danceability  : 0.8
  Tempo Bpm     : 95

============================================
  TOP 5 RECOMMENDATIONS
============================================

1. Concrete Kings — Blocktext
   Score: 4.35
   Why:
     • genre match: hip hop (+1.0)
     • energy near target (+1.38)
     • valence near target (+1.00)
     • danceability near target (+0.47)
     • tempo_bpm near target (+0.50)

2. Velvet Hours — Ivory Lane
   Score: 3.53
   Why:
     • same genre family as hip hop (+0.5)
     • energy near target (+1.16)
     • valence near target (+0.93)
     • danceability near target (+0.45)
     • tempo_bpm near target (+0.49)

3. Island Time — Sunset Palms
   Score: 3.43
   Why:
     • same genre family as hip hop (+0.5)
     • energy near target (+1.26)
     • valence near target (+0.78)
     • danceability near target (+0.47)
     • tempo_bpm near target (+0.41)

4. Night Drive Loop — Neon Echo
   Score: 3.21
   Why:
     • energy near target (+1.42)
     • valence near target (+0.89)
     • danceability near target (+0.46)
     • tempo_bpm near target (+0.43)

5. Rooftop Lights — Indigo Parade
   Score: 3.06
   Why:
     • energy near target (+1.41)
     • valence near target (+0.79)
     • danceability near target (+0.49)
     • tempo_bpm near target (+0.37)


============================================
  EMO RAGER — TASTE PROFILE
============================================
  Genre         : metal
  Energy        : 0.95
  Valence       : 0.05
  Danceability  : 0.1
  Tempo Bpm     : 60

============================================
  TOP 5 RECOMMENDATIONS
============================================

1. Iron Verdict — Ashfall
   Score: 3.57
   Why:
     • genre match: metal (+1.0)
     • energy near target (+1.47)
     • valence near target (+0.79)
     • danceability near target (+0.31)
     • tempo_bpm near target (+0.00)

2. Storm Runner — Voltline
   Score: 2.80
   Why:
     • same genre family as metal (+0.5)
     • energy near target (+1.44)
     • valence near target (+0.57)
     • danceability near target (+0.22)
     • tempo_bpm near target (+0.07)

3. Signal Lost — Grid Runner
   Score: 2.26
   Why:
     • energy near target (+1.40)
     • valence near target (+0.56)
     • danceability near target (+0.13)
     • tempo_bpm near target (+0.18)

4. Night Drive Loop — Neon Echo
   Score: 2.21
   Why:
     • energy near target (+1.20)
     • valence near target (+0.56)
     • danceability near target (+0.18)
     • tempo_bpm near target (+0.27)

5. Concrete Kings — Blocktext
   Score: 2.15
   Why:
     • energy near target (+1.25)
     • valence near target (+0.45)
     • danceability near target (+0.12)
     • tempo_bpm near target (+0.33)


============================================
  OUT OF BOUNDS — TASTE PROFILE
============================================
  Genre         : polka
  Energy        : 1.5
  Valence       : -0.2
  Danceability  : 2.0
  Tempo Bpm     : 300

============================================
  TOP 5 RECOMMENDATIONS
============================================

1. Iron Verdict — Ashfall
   Score: 0.87
   Why:
     • energy near target (+0.70)
     • valence near target (+0.54)
     • danceability near target (+-0.26)
     • tempo_bpm near target (+-0.11)

2. Storm Runner — Voltline
   Score: 0.58
   Why:
     • energy near target (+0.61)
     • valence near target (+0.32)
     • danceability near target (+-0.17)
     • tempo_bpm near target (+-0.19)

3. Signal Lost — Grid Runner
   Score: 0.51
   Why:
     • energy near target (+0.57)
     • valence near target (+0.31)
     • danceability near target (+-0.08)
     • tempo_bpm near target (+-0.29)

4. Neon Alley — Pulse Theory
   Score: 0.41
   Why:
     • energy near target (+0.67)
     • valence near target (+0.08)
     • danceability near target (+-0.04)
     • tempo_bpm near target (+-0.30)

5. Gym Hero — Max Pulse
   Score: 0.34
   Why:
     • energy near target (+0.65)
     • valence near target (+0.03)
     • danceability near target (+-0.06)
     • tempo_bpm near target (+-0.28)
     
```
**Example Output Using Improved Formatting**

```

ROCK HEAVY — TASTE PROFILE
╭──────────────┬─────────╮
│ Attribute    │ Value   │
├──────────────┼─────────┤
│ Genre        │ rock    │
│ Energy       │ 0.9     │
│ Valence      │ 0.55    │
│ Danceability │ 0.5     │
│ Tempo Bpm    │ 130     │
╰──────────────┴─────────╯

TOP 5 RECOMMENDATIONS
+-----+--------------+--------------+---------+--------------------------------------------+
|   # | Title        | Artist       |   Score | Why (top 3 reasons)                        |
+=====+==============+==============+=========+============================================+
|   1 | Storm Runner | Voltline     |    4.23 | energy fit, exact genre match, valence fit |
+-----+--------------+--------------+---------+--------------------------------------------+
|   2 | Iron Verdict | Ashfall      |    3.42 | energy fit, valence fit, same-genre family |
+-----+--------------+--------------+---------+--------------------------------------------+
|   3 | Signal Lost  | Grid Runner  |    3.24 | energy fit, valence fit, tempo fit         |
+-----+--------------+--------------+---------+--------------------------------------------+
|   4 | Neon Alley   | Pulse Theory |    3.04 | energy fit, valence fit, tempo fit         |
+-----+--------------+--------------+---------+--------------------------------------------+
|   5 | Gym Hero     | Max Pulse    |    3.04 | energy fit, valence fit, tempo fit         |
+-----+--------------+--------------+---------+--------------------------------------------+


```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

Initial taste profile consisted of a binary genre: Either selection was target_genre (1) or it was not (0). This meant if say I chose "rock" as the target_genre, a song that was "indie-rock" or "metal-rock" would score a 0 despite them being *similar* to the target_genre.
Adjusted target_genre to incorporate genre *families* where if the genre was an exact match (i.e. rock), it'll be given a 1.0. If it's within the same family, then the song would be given a 0.5 and finally if it's neither, it'll be given a 0.0.

---

## Limitations and Risks

This recommender is intentionally simple, so it has rea limits:
  * **Tiny, uneven catalog**
    * Only 20 songs, and most genres have just one track, so a "winner" is often the *only* option in its genre rather than a truly best match
  * **No Understanding of lyrics, language, era, or artist**
    * It only sees give numeric/label features, so it can't tell a sad-lyrics song from a happy one.
  * **Genre and energy dominate**
    * It can over-favor the user's stated genre (a filter-bubble effect) and lean toward high-energy songs regardless of fit.
  * **Ignores mood andacousticness**
    * Those columns exist in the data but aren't scored, so tastes tied to them can't be expressed.
  * ** No input validation**
    * An impossible or contradictory profile still returns a confident "winner" instead of flagging it.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)
