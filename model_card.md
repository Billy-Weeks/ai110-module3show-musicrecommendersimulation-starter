# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

DownloadDash

---

## 2. Intended Use  

**DownloadDash** is a simple content-based music recommender that takes a listener's profile of their tastes and ranks a catalog of songs to return the top matches, along with a short explanation as to why those specific songs were chosen.

* This app assumes the listener can describe their tastes as numbers on a 0-1 scale (except for tempo BPM), that those preferences are internally consistent, and that a single genre plus four additional attributes (energy, valence (overall happiness), danceability, and tempo) is able to capture the essence of what someone wants to hear. It does *not* learn from listening history, feedback or context (what day/time of day it is, activity like working out, etc).

* This app is built for classroom exploration only. The idea is to understand how a scoring-weighing system works and produces recommendations. As well as to highlight where biases can come from in regards to selecting recommendations.

---

## 3. How the Model Works  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

This model works by taking a few of the main attributes and giving them a rank of how important they are to what would be liked about the song. The listener is able to set these specific attributes to what they enjoy listening too (a target). I.e. someone who really likes songs that are upbeat and happy may score *valence* as a higher number. Not all the chosen attributes matter the same, so energy is given a greater **weight** than say danceability. 

Then a song is, using its already decided values for the same attributes, compared to the target. A song whose values are closer to the target (either less than or greater than) is scored higher for that attribute. *Genre* is handled slightly differently due to it not being a numerical value. Genres are split into families of similar genres. If a song perfectly matches a target genre, then it earns the highest score for that attribute. If a song matches within the same family, it'll earn less and all other cases will receive no points for this attribute. Once all attributes are individually scored, each score is added up and listed in order highest score to lowest. Only the top are given as recommendations. 

Originally, the logic started with genre being completely binary: either the genre matched or it didn't. This gave too much bias to songs that matched in genre and adversely affected songs that might have a genre similar but not exact. Now, genres like *edm* or *synthwave* will have a similarity match with techno. Also, since tempo is in a range of about 60 - 168, it was normalized so it wouldn't overpower the rest of the scores which are scored 0-1.

---

## 4. Data  

The catalog is a small CSV of 20 songs, each labeled with a genre, a mood, and five numeric attributes (energy, tempo, valence, danceability, acousticness). It's deliberately diverse — it spans roughly **17 genres** (pop, indie pop, dream pop, rock, metal, edm, techno, synthwave, lofi, ambient, jazz, folk, classical, country, hip hop, r&b, reggae) and a wide range of moods (happy, chill, intense, moody, melancholy, aggressive, romantic, calm, hypnotic, and more).

I did not remove any songs, only added about 10 songs following the same format of attributes. The attributes as they are currently were also not changed. 

What's missing: the biggest gap is *depth per genre* — most genres have only one song (techno, metal, hip hop, jazz, etc.), so "best techno" is really "the only techno," which makes some winners look more impressive than they are. The data also doesn't capture parts of taste that real listeners care about: lyrics or language, era/decade, artist popularity, or vocal vs. instrumental. And notably, two attributes that are in the data — mood and acousticness — aren't used by the scoring at all, so an acoustic-leaning listener's preference can't actually be expressed yet.

---

## 5. Strengths  

This model/app works best for coherent, mainstream-genre listeners. Profiles whose genre exists in the catalog and whose numeric targets don't contradict each other (unlike the **Emo Rager** and **Out of Bounds** stress tests)

The scoring does well with matching several patterns:

* **Proximity on energy and mood**-> Due to energy and valence having the heaviest numeric weights, the model reliably rewards songs that "feel" right

* **Graceful genre neighbors**-> My genre-family change means that when there isn't a second song in the exact genre, the runner-ups are still *related* styles instead of random picks. 

* **Transparency** Every recommendation comes with a per-feature "why" breakdown, so it's easy to see *why* a song won, making the system interpretable, not a black box.


---

## 6. Limitations and Bias 

The scoring function awards a "genre bonus" which creates a situation where genre pushes songs to the front despite other categories ratings which may conflict. Due to the scoring of +1.0 for an exact genre match, a +0.5 for a familial match, and 0.0 for everything else, a song that matches a user's desired genre will almost always outrank an off-genre song that may match energy, valence, danceability, and tempo better. This causes an almost echo-chamber like effect where the user will constantly be suggested songs from the same genre and narrowing discovery of other genres over time.   

---

## 7. Evaluation  

**Profiles I tested:**
* I ran five profiles: three realistic personas (**Rock Heavy**->rock, loud, **Not Technoblade**-> techno, upbeat, danceable, **Hip Hop-optamus**-> hip hop, groovy, mid-tempo) and two profiles deliberately designed to stress test (**Emo Rager**-> metal, but with contradictory targets: loud yet sad, fast-feeling yet slow, and **Out of Bounds**-> a fake genre and impossible numbers that go out of assumed bounds)

**What I looked for:**
* For each profile I checked whether the #1 song actually matched the persona and whether off-genre songs that fit the _numbers_ well could still sneak into the top 5. All three realistic profiles put the "correct" genre at #1, which was reassuring.

**What surprised me:**
* The stress test profiles surprised me the most. Even though **Emo Rager** was intentionally designed to be contradictory amongst itself, the recommender was still able to output a "winner". While we may understand that the combination of "loud+sad+slow+not danceable" wouldn't normally work, the recommender didn't take that impossibility into consideration. Also **Out of Bounds** didn't catch any of the impossibilities designed into its profile such as negative numbers or made-up genre that didn't exist in the current data. 

This highlighted the fact that as the recommender exists currently there is no validation or error handling and that it just *trusts* any of the inputs given. 

* *Gym Hero* a designated pop song seemed to pop up in profiles that I wouldn't otherwise assume it would: **Rock Heavy** and **Not Technoblade**. Since this song has an extremely high energy score (0.93) and due to how the recommender weighs energy almost as high as genre, it will sneak into a profile that its genre doesn't match. 

**Comparisons:**

* **Rock Heavy vs. Not Technoblade**
  * Rock gets rock (Storm Runner) and techno gets techno (Signal Lost); interestingly Storm Runner appears in both top 5s because both personas want high energy, showing energy crosses genre lines. Makes sense.

* **Rock Heavy vs. Hip Hop-optamus**
  * Rock's winner leans on high energy (0.9) while hip hop's winner (Concrete Kings) wins on a perfect valence match (+1.00) at a much lower tempo (95 vs 130); the profiles correctly pull in opposite tempo/energy directions.

* **Rock Heavy vs. Emo Rager**
  * Both live in the rock/metal family and share Storm Runner and Iron Verdict, but Rock Heavy ranks the rock song first and Emo Rager the metal song first, purely from the exact-genre bonus flipping their order.

* **Rock Heavy vs. Out of Bounds**
  * Rock produces a clean 4.23 winner; Out of Bounds produces a 0.87 "winner" with negative parts, showing how fragile the scoring is once inputs leave the 0–1 range.

* **Not Technoblade vs. Hip Hop-optamus**
  * Techno favors danceable, faster tracks; hip hop favors groovy, slower ones, and each correctly surfaces its own genre first, confirming tempo/danceability are pulling their weight.

* **Not Technoblade vs. Emo Rager**
  * Both want high energy, so both lists share Signal Lost, but the happy techno profile ranks it #1 while the sad metal profile ranks it only #3 because Signal Lost's cheerful valence fits techno better than metal.

* **Not Technoblade vs. Out of Bounds**
  * Same catalog, wildly different scale: a coherent profile tops out near 4.0, the broken one near 0.9, illustrating the score has no fixed floor.

* **Hip Hop-optamus vs Emo Rager**
  * The happy, danceable profile scores its winner highest of all (4.35) while the contradictory profile scores lowest of the realistic-looking runs (3.57), suggesting the total score is a rough signal of how "self-consistent" a profile is.

* **Hip Hop-optamus vs. Out of Bounds**
  * Hip hop's perfect valence match (+1.00) versus Out of Bounds' negative contributions is the clearest before/after of what valid vs. invalid input does to the math.

* **Emo Rager vs. Out of Bounds**
  * Both are adversarial, but Emo Rager fails silently (plausible-looking winner) while Out of Bounds fails loudly (negative numbers), which taught me that quiet failures are the more dangerous kind.


---

## 8. Future Work  

* **Input validation and clamping**
  * The Out of Bounds test showed the model trusts any and all inputs, even impossible ones, producing negative point contributions. Adding range-checking and a feature that assigns the max/min if a value goes outside of the range in either direction would allow the model to defend against those impossible inputs. 

* **Use the features I'm ignoring**
  * _Mood_ and _acousticness_ are in the data but aren't scored and so the `likes_acoustic` doesn't do anything. Adding these would allow quieter or acoustic tastes to expressed.

* **Reduce genre dominance for better diversity**
  * The +1.0 exact-genre bonus creates the filter bubble described previously. Shrinking that bonus, or normalizing it similar to how tempo was normalized, would allow a cross-genre match to compete better than it can now. 

* **Handle contradictory profiles**
  * Have the model flag when no song scores above some threshold instead of allowing a "winner" to be chosen as in the case of **Emo Rager**

* **More depth per genre and richer taste input**
  * Adding several songs per genre would make winners more meaningful rather than "the only one", and future versions could learn from listening history or "likes" instead of relying on hand-set sliders.

---

## 9. Personal Reflection  

During this project I learned more about how music apps/sites like Spotify actually recommend music to its listeners. I always assumed it was pretty involved, however I don't think I fully understood the scope. Even as I did this project which is supposed to be a "simple" version of one of those, I found myself getting into the weeds of balancing importance, what attributes to include (and why!), how to normalize each category which inherently are supposed to be describing the same thing, etc. 

I initially went in knowing that genre matches would be a burden on the scoring system, and I deliberately tried to avoid allowing that. However even with that thought my first skeleton of the model did in fact cause those issues as did my first attempt to "fix" that issue. In fact my misunderstanding of the weights actually caused genre to have such a huge gap that even if a song matched perfectly on all other attributes, it wouldn't get recommended over a song of the same genre that had a huge differences in every other attribute. 

I believe that though this model is "simple" it still did well with recommending songs that, if they were real, would be similar to whatever profile I would set. 

In this project, I did use AI tools heavily in helping me understand what the prompts were asking me to do and/or explain some topics to me (i.e. Valence was something I hadn't heard of before). While attempting the first few steps, I had a feeling that I wasn't understanding something especially when we came to weights and it seemed to be doing the opposite of what I understood it to be doing. Using the agent to describe simply what was being asked or even having it check what I wrote/did was a huge help with this project. 