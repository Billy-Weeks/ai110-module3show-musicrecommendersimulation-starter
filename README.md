# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

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
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

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

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



