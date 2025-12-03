from filare.models.numbers import NumberAndUnit
from filare.models.termination import TerminationEnd, TerminationRow


def test_termination_end_allows_numbers():
    end = TerminationEnd(
        harness="H1",
        connector="J1",
        pin="1",
        splice="SPL1",
        crimp="CR1",
        length=NumberAndUnit(10, "cm"),
        notes="near connector",
    )

    assert end.length.number == 10
    assert end.length.unit == "cm"
    assert end.splice == "SPL1"


def test_termination_row_aggregates_fields():
    from_end = TerminationEnd(harness="H1", connector="J1", pin="1")
    to_end = TerminationEnd(harness="H1", connector="J2", pin="2")
    row = TerminationRow(
        from_end=from_end,
        to_end=to_end,
        wire_id="W1",
        gauge=NumberAndUnit(20, "AWG"),
        color="RD",
    )

    assert row.from_end.connector == "J1"
    assert row.to_end.pin == "2"
    assert row.gauge.unit == "AWG"
    assert row.color == "RD"
