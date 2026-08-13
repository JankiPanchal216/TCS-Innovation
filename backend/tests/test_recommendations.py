from app.services.recommendations.academic import AcademicScorer
from app.services.recommendations.interests import InterestsScorer
from app.services.recommendations.history import HistoryScorer
from app.services.recommendations.collaborative import CollaborativeScorer
from app.services.recommendations.popularity import PopularityScorer
from app.services.recommendations.scoring import ScoringService
from app.services.recommendations.diversity import DiversityReranker

def test_academic_scorer():
    scorer = AcademicScorer({"book_1": 0.9, "book_2": 0.5})
    assert scorer.score({"book_id": "book_1"}) == 0.9
    assert scorer.score({"book_id": "book_3"}) == 0.0

def test_interests_scorer():
    scorer = InterestsScorer(["Cybersecurity", "Machine Learning"])
    
    # Exact match
    assert scorer.score({"categories": ["Cybersecurity"]}) == 0.5
    
    # Multiple matches
    assert scorer.score({"categories": ["Cybersecurity", "Machine Learning"]}) == 1.0
    
    # Case insensitive
    assert scorer.score({"subjects": ["cybersecurity"]}) == 0.5
    
    # No match
    assert scorer.score({"categories": ["Fiction"]}) == 0.0

def test_history_scorer():
    past_books = [
        {"categories": ["Fiction"], "authors": ["Author A"]}
    ]
    scorer = HistoryScorer(past_books)
    
    # Matches author
    assert scorer.score({"authors": ["Author A"]}) >= 0.6
    
    # Matches category
    assert scorer.score({"categories": ["Fiction"]}) >= 0.4
    
    # Matches both
    assert scorer.score({"categories": ["Fiction"], "authors": ["Author A"]}) == 1.0
    
    # No match
    assert scorer.score({"categories": ["Science"]}) == 0.0

def test_collaborative_scorer():
    scorer = CollaborativeScorer({"book_1": 0.8})
    assert scorer.score({"book_id": "book_1"}) == 0.8
    assert scorer.score({"book_id": "book_2"}) == 0.0

def test_cold_start():
    # Cold start: empty interests, no history, no collaborative, no courses
    academic = AcademicScorer({})
    interests = InterestsScorer([])
    history = HistoryScorer([])
    collab = CollaborativeScorer({})
    pop = PopularityScorer({"book_1": 1.0, "book_2": 0.5})
    hybrid = {}
    
    scoring_service = ScoringService(hybrid, academic, interests, history, collab, pop)
    
    candidates = [
        {"book_id": "book_1", "available_copies": 1},
        {"book_id": "book_2", "available_copies": 0}
    ]
    
    scored = scoring_service.score_candidates(candidates)
    
    # Book 1 gets popularity (5% * 1.0) + availability (5% * 1.0) = 0.1
    # Book 2 gets popularity (5% * 0.5) + availability (5% * 0.0) = 0.025
    assert abs(scored[0]["final_score"] - 0.1) < 0.001
    assert scored[0]["book"]["book_id"] == "book_1"
    assert "Popular among all students" in scored[0]["reasons"] or "Currently available" in scored[0]["reasons"]

def test_scoring_weights():
    academic = AcademicScorer({"b1": 1.0})
    interests = InterestsScorer(["A", "C"])
    history = HistoryScorer([{"categories": ["B"], "authors": ["Auth1"]}])
    collab = CollaborativeScorer({"b1": 1.0})
    pop = PopularityScorer({"b1": 1.0})
    hybrid = {"b1": 1.0}
    
    scoring_service = ScoringService(hybrid, academic, interests, history, collab, pop)
    
    # Book b1 is a perfect match on everything
    candidate = {"book_id": "b1", "categories": ["A", "B", "C"], "authors": ["Auth1"], "available_copies": 1}
    scored = scoring_service.score_candidates([candidate])
    
    # Total score should be exactly 1.0 (since it gets 1.0 on every sub-score)
    assert abs(scored[0]["final_score"] - 1.0) < 0.001

def test_diversity_reranker():
    reranker = DiversityReranker(max_per_category=2)
    
    scored_candidates = [
        {"book": {"book_id": "1", "categories": ["A"]}, "final_score": 0.9},
        {"book": {"book_id": "2", "categories": ["A"]}, "final_score": 0.8},
        {"book": {"book_id": "3", "categories": ["A"]}, "final_score": 0.7}, # Should be skipped
        {"book": {"book_id": "4", "categories": ["B"]}, "final_score": 0.6},
        {"book": {"book_id": "5", "categories": ["C"]}, "final_score": 0.5},
        {"book": {"book_id": "6", "categories": ["A"]}, "final_score": 0.4}, # Should be skipped
    ]
    
    final_list = reranker.rerank(scored_candidates, limit=4)
    
    ids = [c["book"]["book_id"] for c in final_list]
    assert ids == ["1", "2", "4", "5"]

def test_deterministic_ranking():
    academic = AcademicScorer({})
    interests = InterestsScorer([])
    history = HistoryScorer([])
    collab = CollaborativeScorer({})
    pop = PopularityScorer({})
    
    scoring_service = ScoringService({}, academic, interests, history, collab, pop)
    
    # Ensure same inputs always produce identical output
    c1 = {"book_id": "1", "available_copies": 1}
    c2 = {"book_id": "2", "available_copies": 0}
    
    run1 = scoring_service.score_candidates([c1, c2])
    run2 = scoring_service.score_candidates([c1, c2])
    
    assert run1 == run2

if __name__ == "__main__":
    print("Running tests...")
    test_academic_scorer()
    test_interests_scorer()
    test_history_scorer()
    test_collaborative_scorer()
    test_cold_start()
    test_scoring_weights()
    test_diversity_reranker()
    test_deterministic_ranking()
    print("All tests passed successfully!")

