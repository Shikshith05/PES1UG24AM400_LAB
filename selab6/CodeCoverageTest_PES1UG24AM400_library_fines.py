# Code (line) coverage tests for library_fines.py
# Name: SHIKSHITH V   SRN: PES1UG24AM400
# Goal: execute every line of library_fines.py at least once.

import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------
def test_returned_on_time():
    assert late_fine("student", 10, False) == 0


def test_unknown_member_raises():
    with pytest.raises(ValueError):
        late_fine("alien", 5, False)


def test_negative_days_raises():
    with pytest.raises(ValueError):
        late_fine("student", -1, False)


def test_faculty_on_time():
    # covers the faculty loan_days = 30 line
    assert late_fine("faculty", 20, False) == 0


def test_guest_overdue_fine_capped_and_damaged():
    # 114 - 14 = 100 days overdue * 5 = 500 -> capped at 200, +150 damage
    assert late_fine("guest", 114, True) == 350


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True


def test_cannot_borrow_with_high_fine():
    assert can_borrow(1, 150, "student") is False


def test_faculty_can_borrow():
    assert can_borrow(5, 0, "faculty") is True


# ---------- renewal_status ----------
def test_renewal_denied_when_reserved():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_overdue():
    assert renewal_status(1, False, -3) == "overdue"


def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"
