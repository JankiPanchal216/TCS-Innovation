# User Search Context

The student dashboard collects structured context to personalize search without requiring the student to type a long paragraph.

## Context Elements
1. **Profile Data (Persistent)**: Department, semester, academic year, interests, reading level, preferred language.
2. **Current Context (Transient)**: Current course, current goal, exam preparation.
3. **Behavioral Signals (Derived)**: Views, saves, borrows, ratings (collected via interactions).

## Implementation
The frontend sends a `context` object in the `/api/search` payload:
```json
{
  "use_profile": true,
  "use_courses": true,
  "use_interests": true,
  "profile": {
    "department": "Computer Science",
    "current_courses": ["Operating Systems"],
    "interests": ["Security"]
  }
}
```
This context is ingested by the `HybridSearchService` after candidate retrieval, boosting the relevance score of matching books while strictly enforcing any hard filters specified in the `filters` block.
