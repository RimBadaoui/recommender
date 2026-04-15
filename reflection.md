# Profile Comparison Reflection

## Profiles Tested

Four user profiles were run against the 15-song catalog:

1. **High-Energy Pop** — `genre=pop, mood=happy, energy=0.9`
2. **Chill Lofi** — `genre=lofi, mood=chill, energy=0.35`
3. **Deep Intense Rock** — `genre=rock, mood=intense, energy=0.92`
4. **Edge Case: High Energy + Sad Mood** — `genre=synthwave, mood=sad, energy=0.95`

---

## Profile 1 vs Profile 2 — Pop/Happy vs Lofi/Chill

These two profiles produced completely different top results with no overlap in the top 3. The pop profile surfaced Sunrise City, Gym Hero, and Rooftop Lights. The lofi profile surfaced Library Rain, Midnight Coding, and Forest Path.

This makes sense: genre is the heaviest weight (+2.0), and pop and lofi are entirely different genre buckets. No song belongs to both, so the two shortlists are fully separated. The energy targets are also opposite ends of the scale (0.9 vs 0.35), which further pushes the two profiles apart.

What this tells us: the scoring logic correctly separates users with very different tastes. For profiles that are clearly different, the system works as expected.

---

## Profile 1 vs Profile 3 — Pop/Happy vs Rock/Intense

The pop and rock profiles share a similar energy target (0.9 vs 0.92), but their genres and moods are different. Despite this, Gym Hero appeared in both top-5 lists — at #2 for pop (score 2.97) and #3 for rock/intense (score 1.99).

Why? Gym Hero has `genre=pop` and `mood=intense` and `energy=0.93`. For the pop profile it earned genre match (+2.0) and near-perfect energy. For the rock profile it earned mood match (+1.0) and near-perfect energy, but no genre match. The same song is a strong fit for one profile and a decent fit for the other because it straddles two of the scoring dimensions.

What this tells us: a song can serve multiple profiles when its features cross over category lines. This is actually realistic — "Gym Hero" genuinely feels at home in both a pop playlist and an intense workout playlist.

---

## Profile 3 vs Profile 4 — Rock/Intense vs Synthwave/Sad

These two profiles have nearly identical energy targets (0.92 vs 0.95) but different genres and moods. The rock profile returned Voltline songs at the top. The synthwave profile returned Ultraviolet and Night Drive Loop.

The key difference: the sad mood in Profile 4 **never fired** because no song in the catalog has `mood=sad`. The top score for the synthwave/sad profile was only 2.84 (genre + energy only), while the rock/intense profile reached 3.99 (genre + mood + energy). The sad profile is structurally handicapped — it can never earn the +1.0 mood bonus regardless of which song it evaluates.

This is the most important finding: two profiles with similar energy levels produce very different score ceilings depending on whether their mood exists in the catalog. A user asking for "sad" music gets confidently wrong results — the system never signals that something is missing.

---

## Overall Takeaway

The scoring logic works well when the user's preferences map cleanly onto the catalog. When a preference (like "sad" mood) has no representation in the data, the system does not fail visibly — it just silently returns the best available match, which may be emotionally or aesthetically wrong. This is a bias embedded in the data, not the algorithm, but the algorithm has no way to surface it.
