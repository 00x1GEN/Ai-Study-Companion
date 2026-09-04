from app.services.gamification_service import level_for_xp, level_progress

def test_levels():
    assert level_for_xp(0) == 1
    assert level_for_xp(99) == 1
    assert level_for_xp(100) == 2
    assert level_for_xp(550) == 6

def test_level_progress():
    assert level_progress(0) == 0
    assert level_progress(50) == 0.5
    assert level_progress(150) == 0.5
