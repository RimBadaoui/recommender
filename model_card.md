# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system suggests up to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration — to demonstrate how a simple scoring rule can produce ranked recommendations — and is not intended for real users or production music apps.

**Not intended for:** personalized recommendations at scale, users with diverse or evolving taste, or any context where fairness or representation across genres matters.

---

## 3. How the Model Works

VibeFinder looks at three things about each song and compares them to what the user said they like:

1. **Genre**: If the song's genre matches the user's favorite, it gets 2 points. This is the biggest factor.
2. **Mood**: If the song's mood matches (happy, chill, intense, etc.), it gets 1 point.
3. **Energy**: Every song gets a partial score based on how close its energy level (0.0 to 1.0) is to the user's target. A perfect match gives 1 point; a song at the opposite end of the scale gives close to 0.

All three scores are added together. The maximum is 4.0. The songs are then sorted from highest to lowest score, and the top results become the recommendations. Each result also shows which rules fired, so you can see exactly why a song was chosen.

---

## 4. Data

- **Catalog size**: 15 songs
- **Original dataset**: 10 songs provided as a starter file
- **Added**: 5 songs to increase variety (Desert Wind, Neon Jungle, Sunday Brunch, Ultraviolet, Forest Path)
- **Genres represented**: pop, lofi, rock, ambient, jazz, synthwave, indie pop
- **Moods represented**: happy, chill, intense, relaxed, focused, moody
- **Missing moods**: sad, angry, nostalgic, romantic — these are absent from the catalog entirely
- **Whose taste**: the dataset skews toward Western pop and electronic music; jazz and ambient have only 1–2 songs each, and no hip-hop, classical, or R&B is represented

---

## 5. Strengths

- **Well-served profiles**: users whose taste matches a well-represented genre (pop, lofi, rock) get intuitive top results. The chill lofi profile, for example, achieves a near-perfect score of 4.00 on "Library Rain."
- **Transparent**: every recommendation comes with a plain-language reason ("genre match (+2.0), mood match (+1.0), energy similarity +0.92"), so the user can always understand why a song appeared.
- **Simple and predictable**: because the rules are hand-written, there are no hidden weights or black-box behavior. You can read the code and predict the output.

---

## 6. Limitations and Bias

- **Genre weight is too strong**: at +2.0, a genre match alone outweighs mood + energy combined. A mediocre song in the right genre will always beat a great song in the wrong genre, even if the wrong-genre song matches perfectly on every other dimension.
- **Missing moods cause silent failure**: if the user's preferred mood doesn't exist in the catalog (e.g., "sad"), the mood rule never fires and no warning is shown. The system quietly returns wrong results with confidence.
- **No diversity control**: the same artist can occupy multiple top-5 slots. The rock/intense profile returns Voltline at #1 and #2 with no mechanism to spread recommendations across different artists.
- **Small catalog amplifies bias**: with only 1–2 jazz or ambient songs, users who prefer those genres get a very limited and repetitive set of results, even if the scores are technically correct.
- **Energy is a weak tiebreaker**: since it can only add up to 1.0 point, it mostly separates songs that already tied on genre/mood. It cannot rescue a song that missed on both genre and mood.
- **No learning**: the system treats every user identically except for the three profile fields. It has no concept of listening history, skips, or changing taste.

---

## 7. Evaluation

Four user profiles were tested:

| Profile | Top Result | Score | Notes |
|---|---|---|---|
| High-Energy Pop | Sunrise City | 3.92 | Correct — genre + mood + close energy |
| Chill Lofi | Library Rain | 4.00 | Perfect score — all three rules fired |
| Deep Intense Rock | Storm Runner | 3.99 | Correct — two Voltline songs dominate top 2 |
| High Energy + Sad Mood | Ultraviolet | 2.84 | Incorrect feel — no sad songs exist, mood rule never fired |

The first three profiles matched intuition well. The fourth (adversarial) profile exposed the silent-failure problem: the system returned high-energy synthwave songs that match the energy and genre but completely miss the emotional intent.

Two automated tests were also written and pass:
- `test_recommend_returns_songs_sorted_by_score` — verifies the pop/happy song ranks first for a matching profile
- `test_explain_recommendation_returns_non_empty_string` — verifies explanations are always produced

---

## 8. Future Work

1. **Add a diversity rule**: penalize recommending the same artist twice in the top-5 so results feel more varied.
2. **Rebalance genre weight**: reduce from +2.0 to +1.5 and increase mood to +1.5 to make emotional feel matter as much as genre category.
3. **Expand the catalog**: add hip-hop, classical, R&B, and more mood variety (especially sad and nostalgic) so underserved profiles get real results.
4. **Warn on missing mood**: if the user's target mood doesn't exist in any song in the catalog, print a warning so the user knows the mood rule is not active.
5. **Add user history**: track which songs a user has already heard and down-rank repeats.

---

## 9. Personal Reflection

The most surprising thing about building VibeFinder was how quickly a few lines of addition and comparison started to feel like a real recommender. Sorting a list by a number is not intelligent, but the output looks intelligent — and that gap between appearance and reality is exactly what makes AI systems tricky to evaluate.

The edge-case profile (high energy + sad mood) was the clearest learning moment. There are no sad songs in the catalog, so the system returned technically valid but emotionally wrong results. It did not crash or warn. It just confidently recommended the wrong thing. Real recommendation systems can fail the same way when a demographic group, genre, or preference is underrepresented in training data — the system doesn't know what it doesn't know.

Human judgment still matters for deciding what features to use, what weights to assign, and — most importantly — what is missing from the data. No algorithm can surface preferences it has never seen.
