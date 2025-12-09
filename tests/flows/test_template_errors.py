import pytest

from filare.errors import UnknownTemplateDesignator
from filare.flows.build_harness import build_harness_from_files


def test_unknown_template_reports_known_options(tmp_path):
    bad_yaml = tmp_path / "bad.yml"
    bad_yaml.write_text(
        "connectors: {}\ncables: {}\nconnections:\n  -\n    - UNKNOWN: 1\n    - W1: 1\n"
    )
    extra_metadata = {
        "output_dir": tmp_path,
        "output_name": "bad",
        "sheet_total": 1,
        "sheet_current": 1,
        "sheet_name": "bad",
        "files": [],
        "output_names": [],
        "titlepage": tmp_path / "titlepage",
        "use_qty_multipliers": False,
        "multiplier_file_name": "quantity_multipliers.txt",
    }
    with pytest.raises(UnknownTemplateDesignator) as excinfo:
        build_harness_from_files(
            inp=[bad_yaml],
            metadata_files=[],
            output_formats=("tsv",),
            output_dir=tmp_path,
            extra_metadata=extra_metadata,
            shared_bom={},
        )
    msg = str(excinfo.value)
    assert "UNKNOWN" in msg
    assert "known connectors" in msg or "known cables" in msg
