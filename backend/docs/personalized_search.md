# Personalized Search

Personalized Search runs as a final re-ranking step after the Reciprocal Rank Fusion (RRF) of Keyword and Semantic search.

## Formula
`personalized_score = 0.50 * rrf + 0.15 * academic + 0.15 * interest + 0.10 * history + 0.05 * popularity + 0.05 * availability`

## Components
- **RRF Score**: Base relevance from query matching.
- **Academic Score**: +1.0 if the book matches a user's current course, +0.5 if it matches their department.
- **Interest Score**: +1.0 if the book matches a user's stated interests.
- **Availability Score**: +1.0 if `available_copies > 0`.

The API returns `explanation_factors` for transparency (e.g., "Matches your academic courses/department").
