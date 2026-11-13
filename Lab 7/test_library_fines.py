import string
from hypothesis import given, strategies as st
from library_fines import parse_member_id, total_fine, shelf_code

# Inputs of every kind: text, None, numbers, lists
ANY_INPUT = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.lists(st.integers()),
)

# ---------- parse_member_id ----------
@given(st.text() | st.none())
def test_parse_member_id_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed with: {e}"

@given(ANY_INPUT)
def test_parse_member_id_any_type_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed on {s!r} with: {e}"

@given(st.from_regex(r"[A-Za-z]{1,10}-[0-9]{1,9}", fullmatch=True))
def test_parse_member_id_valid_format(s):
    member_type, number = parse_member_id(s)
    prefix, digits = s.split("-")
    assert member_type == prefix.upper()
    assert number == int(digits)

# ---------- total_fine ----------
@given(st.text() | st.none())
def test_total_fine_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed with: {e}"

@given(ANY_INPUT)
def test_total_fine_any_type_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed on {s!r} with: {e}"

@given(st.lists(st.integers(min_value=0, max_value=10000)))
def test_total_fine_valid_property(days):
    result = total_fine(",".join(str(d) for d in days))
    assert result == sum(max(d - 14, 0) * 2 for d in days)
    assert result >= 0

# ---------- shelf_code ----------
@given(st.text() | st.none())
def test_shelf_code_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed with: {e}"

@given(ANY_INPUT)
def test_shelf_code_any_type_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed on {s!r} with: {e}"

WORD = st.text(alphabet=string.ascii_letters, min_size=1, max_size=10)

@given(WORD, WORD)
def test_shelf_code_valid_property(a, b):
    assert shelf_code(f"{a} {b}") == (a[0] + b[0]).upper()