import pytest

from app import build_properties

MAP = {"Name": "title", "Priority": "number", "Status": "select", "Due": "date", "Done": "checkbox"}


def test_build_properties():
    row = {"Name": "Fix bug", "Priority": "2", "Status": "Todo", "Due": "2026-11-01", "Done": "yes"}
    p = build_properties(row, MAP)
    assert p["Name"]["title"][0]["text"]["content"] == "Fix bug"
    assert p["Priority"]["number"] == 2.0 and p["Done"]["checkbox"] is True


def test_empty_values_skipped_and_bad_type():
    assert "Priority" not in build_properties({"Name": "x", "Priority": ""}, MAP)
    with pytest.raises(ValueError):
        build_properties({"A": "1"}, {"A": "weird"})
