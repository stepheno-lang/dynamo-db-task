import json
from pathlib import Path

OUTPUT = Path("output")


def test_required_files_exist():
    assert (OUTPUT / "path.json").exists()
    assert (OUTPUT / "summary.json").exists()
    assert (OUTPUT / "validation.json").exists()


def test_path_json():
    data = json.loads((OUTPUT / "path.json").read_text())

    assert isinstance(data, list)
    assert len(data) >= 2

    for node in data:
        assert isinstance(node, dict)
        assert "package" in node
        assert "version" in node

        assert isinstance(node["package"], str)
        assert isinstance(node["version"], str)


def test_summary_json():
    data = json.loads((OUTPUT / "summary.json").read_text())

    assert set(data.keys()) == {
        "total_cost",
        "path_length",
        "valid",
    }

    assert isinstance(data["total_cost"], (int, float))
    assert isinstance(data["path_length"], int)
    assert isinstance(data["valid"], bool)


def test_validation_json():
    data = json.loads((OUTPUT / "validation.json").read_text())

    assert set(data.keys()) == {
        "constraints_satisfied",
        "minimum_cost",
    }

    assert isinstance(data["constraints_satisfied"], bool)
    assert isinstance(data["minimum_cost"], bool)