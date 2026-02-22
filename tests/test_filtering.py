from job_scraping_codx.tech_filter import relevance_label, relevance_score


def test_relevance_score_high_for_tech_text() -> None:
    text = "Software Engineer internship with Python, React and AWS"
    assert relevance_score(text) >= 0.6
    assert relevance_label(relevance_score(text)) == "tech_relevant"


def test_relevance_score_low_for_non_tech_text() -> None:
    text = "Sales executive role in real estate with field travel"
    assert relevance_score(text) < 0.3
    assert relevance_label(relevance_score(text)) == "not_tech_relevant"
