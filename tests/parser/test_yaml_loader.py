import pytest
import yaml

from filare.parser.yaml_loader import (
    merge_content,
    merge_item,
    parse_concat_merge_files,
    parse_merge_files,
    parse_merge_yaml,
    safe_load_yaml,
)


def test_merge_item_prefers_y_over_x_for_scalars():
    assert merge_item(1, 2) == 2
    assert merge_item({"a": 1}, {"a": 2})["a"] == 2


def test_merge_content_combines_lists_and_dicts():
    x = {"a": 1, "b": [1, 2], "c": {"k": "v"}}
    y = {"b": [3], "c": {"k": "v2"}}
    merged = merge_content([x, y])
    assert merged["b"] == [1, 2, 3]
    assert merged["c"]["k"] == "v2"


def test_parse_merge_yaml_overrides_ints_to_str():
    data = """
    a: 1
    b: 2
    """
    merged = parse_merge_yaml([data])
    assert merged["a"] == "1"
    assert merged["b"] == "2"


def test_safe_load_yaml_rejects_invalid(tmp_path):
    bad_yaml = tmp_path / "bad.yml"
    bad_yaml.write_text("a: [1,")
    with pytest.raises(yaml.YAMLError):
        safe_load_yaml([bad_yaml.read_text()])


def test_parse_merge_files_reads_files(tmp_path):
    f1 = tmp_path / "a.yml"
    f2 = tmp_path / "b.yml"
    f1.write_text("a: 1")
    f2.write_text("b: 2")
    merged = parse_merge_files([f1, f2])
    assert merged == {"a": "1", "b": "2"}


def test_parse_concat_merge_files_concats_then_merges(tmp_path):
    f1 = tmp_path / "a.yml"
    f2 = tmp_path / "b.yml"
    m = tmp_path / "meta.yml"
    f1.write_text("a: 1")
    f2.write_text("b: 2")
    m.write_text("c: 3")
    merged = parse_concat_merge_files([f1, f2], [m])
    assert merged["a"] == "1"
    assert merged["b"] == "2"
    assert merged["c"] == "3"


def test_parse_merge_yaml_handles_empty_list():
    assert parse_merge_yaml([]) == {}


def test_merge_item_handles_none_and_type_mismatch():
    assert merge_item({"a": 1}, None) == {"a": 1}
    assert merge_item(None, {"a": 2}) == {"a": 2}
    # when types differ, y wins
    assert merge_item({"a": 1}, ["b"]) == ["b"]


def test_merge_item_lists_are_concatenated():
    assert merge_item([1, 2], [3, 4]) == [1, 2, 3, 4]
