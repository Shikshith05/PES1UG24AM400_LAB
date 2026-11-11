# Branch coverage tests for library_fines.py
# Name: SHIKSHITH V   SRN: PES1UG24AM400
# Goal: make every if / elif / else decision evaluate to BOTH True and False.

import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ================= late_fine =================
# Decision 1: member not in DAILY_FINE
def test_unknown_member_raises():                 # True branch
    with pytest.raises(ValueError):
        late_fine("alien", 5, False)


def test_known_member_student():                  # False branch
    assert late_fine("student", 10, False) == 0


# Decision 2: days_kept < 0
def test_negative_days_raises():                  # True branch
    with pytest.raises(ValueError):
        late_fine("guest", -1, False)


def test_zero_days_is_valid():                    # False branch (boundary)
    assert late_fine("guest", 0, False) == 0


# Decision 3: member == "faculty"  (if / else)
def test_faculty_loan_period_30_days():           # True branch
    assert late_fine("faculty", 30, False) == 0   # last day of loan
    assert late_fine("faculty", 31, False) == 1   # 1 day overdue * 1


def test_non_faculty_loan_period_14_days():       # False branch
    assert late_fine("student", 14, False) == 0   # last day of loan
    assert late_fine("student", 15, False) == 2   # 1 day overdue * 2


# Decision 4: overdue > 0
def test_not_overdue_no_fine():                   # False branch
    assert late_fine("guest", 5, False) == 0


def test_overdue_fine_below_cap():                # True branch + cap False
    # 24 - 14 = 10 days * 5 = 50 (not capped)
    assert late_fine("guest", 24, False) == 50


# Decision 5: fine > 200
def test_fine_exactly_200_not_capped():           # False branch (boundary)
    # 54 - 14 = 40 days * 5 = 200
    assert late_fine("guest", 54, False) == 200


def test_fine_above_200_is_capped():              # True branch
    # 100 - 14 = 86 days * 5 = 430 -> capped at 200
    assert late_fine("guest", 100, False) == 200


# Decision 6: is_damaged
def test_damaged_book_on_time():                  # True branch, no overdue
    assert late_fine("student", 5, True) == 150


def test_damaged_and_capped_overdue():            # True branch with overdue
    assert late_fine("guest", 114, True) == 350


def test_not_damaged():                           # False branch
    assert late_fine("faculty", 40, False) == 10


# ================= can_borrow =================
# Decision 1: pending_fine > 100
def test_cannot_borrow_high_fine():               # True branch
    assert can_borrow(0, 101, "faculty") is False


def test_fine_exactly_100_allowed():              # False branch (boundary)
    assert can_borrow(0, 100, "student") is True


# Decision 2: member == "faculty"
def test_faculty_under_limit():                   # True branch, returns True
    assert can_borrow(9, 0, "faculty") is True


def test_faculty_at_limit():                      # True branch, returns False
    assert can_borrow(10, 0, "faculty") is False


def test_student_under_limit():                   # False branch, returns True
    assert can_borrow(2, 0, "student") is True


def test_guest_at_limit():                        # False branch, returns False
    assert can_borrow(3, 0, "guest") is False


# ================= renewal_status =================
# Decision 1: has_reservation
def test_reserved_book_denied():                  # True branch
    assert renewal_status(0, True, 5) == "denied"


# Decision 2: times_renewed >= 2
def test_limit_reached_at_two():                  # True branch (boundary)
    assert renewal_status(2, False, 5) == "limit reached"


def test_limit_reached_above_two():               # True branch
    assert renewal_status(5, False, -1) == "limit reached"


# Decision 3: elif days_left < 0
def test_overdue_renewal():                       # True branch
    assert renewal_status(1, False, -1) == "overdue"


def test_renewed_successfully():                  # False branch for all
    assert renewal_status(1, False, 0) == "renewed"
