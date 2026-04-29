# 🎵 Music Recommender Simulation

## Project Summary

This project builds a small music recommender system in Python. It loads a catalog of 15 songs from a CSV file, scores each song against a user taste profile using a weighted rule system, and returns a ranked list of the top recommendations with plain-language explanations. The system demonstrates how simple math can power surprisingly intuitive suggestions — and where bias and limitations still show up.

---

## How The System Works

Real-world recommendation systems typically work in two stages: retrieval (narrowing millions of items to a shortlist) followed by ranking (scoring candidates with context-aware logic). This simulation focuses on the **ranking stage**.

### Data Flow

```
Input (User Prefs: genre, mood, energy)
       │
       ▼
Load all songs from data/songs.csv
       │
       ▼
For every song — score_song(song, user_prefs)
  ├── genre match?   → +2.0 points
  ├── mood match?    → +1.0 point
  └── energy close?  → +0.0 to +1.0  (1 - |song_energy - target_energy|)
       │
       ▼
Sort all songs by score descending
       │
       ▼
Output: Top K songs with scores and reason strings
```

### Algorithm Recipe

Genre matches `favorite_genre` : +2.0 |
Mood matches `favorite_mood` : +1.0 |
Energy similarity = 1 − \|song_energy − target_energy\| | +0.0 to +1.0 |
**Max possible score** | **4.0** 

### Song Features Used

`genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, `artist`

### UserProfile Stores

`favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

### Recommender Scoring

`Recommender.recommend()` calls `_score()` for every song, sorts by score descending, and returns the top k `Song` objects. `explain_recommendation()` returns the same reason string in plain language.

### Potential Biases

- **Genre dominates**: worth +2.0, it can never be overcome by mood + energy alone (+2.0 max combined). A great song in the wrong genre will always rank below a mediocre song in the right genre.
- **No mood in catalog = no mood points**: the edge-case "sad" profile never earns mood points because no songs have `mood=sad`, so the system silently falls back to genre + energy only.
- **Artist clustering**: with no diversity rule, the same artist can fill all top-5 slots.

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

3. Set API Key 

```bash
set GEMINI_API_KEY=YOUR_KEY
```

4. Run the app:
```bash
python main.py --interactive
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

- **Default weights (genre +2.0, mood +1.0, energy +0–1)**: genre dominates. A genre-matched song with wrong mood still beats a mood-matched song in a different genre.
- **Edge case — conflicting prefs** (`synthwave` genre, `sad` mood, `energy=0.95`): no songs carry `mood=sad`, so the mood rule never fires. The system falls back to genre + energy, and the top results feel tonally wrong — they are high-energy synthwave, not emotionally sad.
- **Artist clustering**: the rock/intense profile puts two Voltline songs at #1 and #2 with no other artists near them, showing the system has no diversity protection.

---

## Limitations and Risks

- Only works on a 15-song catalog — niche genres have 1–2 representatives
- Does not understand lyrics, tempo feel, or cultural context
- Over-prioritizes genre: the +2.0 weight means mood and energy together barely compete
- No diversity rule — same artist can dominate all top slots
- Cold-start: a new user must describe their taste manually; no learning from history

---

## Reflection

Building this system made it clear that recommendations are just math disguised as intuition. Assigning a number to "genre match" and sorting by it produces results that *feel* meaningful — but the weights are arbitrary choices that embed real bias. A genre weight of 2.0 quietly says "genre matters twice as much as mood," which may not be true for every listener.

The most surprising moment was the edge-case "sad + high energy" profile. No song in the catalog has a sad mood, so the mood rule silently never fires. The system returned high-energy synthwave songs that match nothing about the emotional intent — and it did so with complete confidence, showing no warning. Real AI systems can fail the same way: a missing data category doesn't cause an error, it just produces a quietly wrong answer.

See [model_card.md](model_card.md) and [reflection.md](reflection.md) for full documentation.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

