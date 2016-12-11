import analyze_comments

def test_compute_rating():
    assert analyze_comments.compute_rating(0, 0, 0) == 'NEUTRAL'
    assert analyze_comments.compute_rating(1, 1, 1) == 'NEUTRAL'
    assert analyze_comments.compute_rating(4, 0, 0) == 'NEUTRAL'
    assert analyze_comments.compute_rating(0, 0, 4) == 'NEUTRAL'
    assert analyze_comments.compute_rating(5, 0, 0) == 'POSITIVE'
    assert analyze_comments.compute_rating(4, 0, 1) == 'POSITIVE'
    assert analyze_comments.compute_rating(3, 0, 2) == 'CONTROVERSIAL'
    assert analyze_comments.compute_rating(2, 1, 2) == 'CONTROVERSIAL'
    assert analyze_comments.compute_rating(2, 2, 1) == 'NEUTRAL'
    assert analyze_comments.compute_rating(1, 3, 1) == 'NEUTRAL'
    assert analyze_comments.compute_rating(1, 2, 2) == 'NEUTRAL'
    assert analyze_comments.compute_rating(2, 0, 3) == 'CONTROVERSIAL'
    assert analyze_comments.compute_rating(1, 0, 4) == 'NEGATIVE'
    assert analyze_comments.compute_rating(0, 0, 5) == 'NEGATIVE'
