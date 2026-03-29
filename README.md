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

Each song is scored against a user profile using four features: `genre` (+2.0 for a match), `mood` (+1.0 for a match), `energy` and `valence` (proximity score: `1 - abs(song_value - user_target)`), and an acoustic bonus (+0.5). Max score is 5.0. Songs are ranked using a min heap to return the top-k results.

**Potential biases:** genre's high weight can overshadow strong mood/energy matches, and exact string matching means `"chill"` and `"relaxed"` are treated as completely different moods.

## Why some songs are ranked #1

For recommendations for Late Night, the system recommended "Focus Flow" as its attributes almost perfectly aligned with the weights and characteristics we made the model prioritize. For every song in the dataset, the model ran it through the score_song function where it compared its attributes to each preference of a user. In Late Night's case, it perfectly matched Focus Flow with the characteristics for a Late Night song as the song's genre was Lofi, mood was focused, an the energies were within 0.99 proximity. Because the song was essentially a perfect match, the model ranked it with the highest score.

## Experiment

We see that weight for genre is the highest. Reducing its weight could then recommend songs that fit the vibe, even if the genre differs. For Sunday Morning, which fits jazz or relaxed mood, Coffee Shop Stories currently wins with the highest recommendation because of the +2.0 genre weight bonus. Changing it to 0.5, we can predict that the songs Library Rain and Spacewalk Thoughts (currently #2 and #3 at ~1.9) would close the gap significantly as they are songs that feel like Sunday morning without being jazz.

## Limitations

Road Trip gets Storm Runner (#1) despite a valence mismatch:
- Road Trip target_valence = 0.60
- Storm Runner valence     = 0.48   → gap of 0.12

Storm Runner ranks #1 purely because of the genre match (+2.0). Its valence is noticeably darker than the user wants, a road trip at 0.48 valence is more "brooding highway" than "windows-down fun." The genre weight is strong enough to override the emotional mismatch.

## Unexpected Results

Party Vibes profile: hip-hop, upbeat, energy=0.90, valence=0.80

Gold Chain Bounce correctly lands at #1 (genre match + near-perfect energy/valence). But #2 and #3 are Gym Hero and Sunrise City, which are both pop, and neither matching genre or mood.

Why? The catalog has only one hip-hop song. Once Gold Chain Bounce is taken, the heap falls back entirely on numerical proximity. Gym Hero scores 1.455 just from energy (0.97) and valence (0.97) proximity alone, which results in no categorical match at all.

This shows that with a small catalog, the system degrades gracefully into a pure vibe-matcher when genre coverage runs out, which is actually reasonable behavior, but it exposes the small catalog bias noted in the README. A real system would have dozens of hip-hop options to fill those slots properly.

## Final Thoughts

This show project is awesome! It really reminds me of my first data science class where we had to build a recommendation system, and it felt very familiar. The biggest main learning point for me was the actual getting the highest scored songs, which is essentially the top k most frequent elements Leetcode problem. The heap is very useful for space and in the case of a large dataset, it is very efficient of only being considered with K elements. Although this project felt purely algorithmic, it still feels like a recommendation system, but just without the parameters for machine learning. If I were to extend this project, I would go towards the AI route and utilize possibly linear regression to determine which weights can minimize prediction errors. 