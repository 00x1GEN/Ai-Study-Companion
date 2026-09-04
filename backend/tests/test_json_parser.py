from app.ai.json_utils import parse_json_array

def test_parse_plain_json_array():
    assert parse_json_array('[{"a":1}]') == [{"a":1}]

def test_parse_fenced_json_array():
    assert parse_json_array('```json\n[{"a":1}]\n```') == [{"a":1}]
