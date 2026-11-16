# Validates the portfolio's CSV deliverables: both files must parse,
# the test-case file must hold the full 24 cases, and every defect ID
# referenced by a test case must exist in the defect log.
import csv, os, sys
BASE = os.path.join(os.path.dirname(__file__), "..")

with open(os.path.join(BASE, "03-test-cases", "test-cases.csv"), newline="", encoding="utf-8") as f:
    cases = list(csv.DictReader(f))
assert len(cases) == 24, f"expected 24 test cases, found {len(cases)}"
for c in cases:
    assert c["Result"] in ("Pass", "Fail", "Blocked"), c
print(f"test-cases.csv: 24 cases OK ({sum(1 for c in cases if c['Result']=='Pass')} pass, "
      f"{sum(1 for c in cases if c['Result']=='Fail')} fail)")

with open(os.path.join(BASE, "08-jira", "jira-tickets.csv"), newline="", encoding="utf-8") as f:
    tickets = list(csv.DictReader(f))
assert len(tickets) >= 10, f"expected at least 10 Jira tickets, found {len(tickets)}"
print(f"jira-tickets.csv: {len(tickets)} tickets OK")

defect_log = open(os.path.join(BASE, "05-defects", "defect-log.md"), encoding="utf-8").read()
for c in cases:
    if c["DefectID"]:
        assert c["DefectID"] in defect_log, f"{c['DefectID']} missing from defect log"
print("All referenced defects exist in the defect log. Validation PASSED.")
