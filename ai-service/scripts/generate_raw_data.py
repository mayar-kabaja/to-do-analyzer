"""
Generate 500+ rows of sample task data for raw_tasks.csv.
Run from ai-service: python scripts/generate_raw_data.py
"""
import csv
import random
from pathlib import Path

OUT = Path(__file__).parent.parent / "data" / "raw_tasks.csv"

TASKS = [
    # Work - high
    ("Finish quarterly report by Friday", "high", "Work"),
    ("Prepare client presentation for Monday", "high", "Work"),
    ("Urgent: fix production bug", "high", "Work"),
    ("Submit project proposal before deadline", "high", "Work"),
    ("Critical: review merger documents", "high", "Work"),
    ("ASAP: respond to client email", "high", "Work"),
    ("Deadline: complete sprint deliverables", "high", "Work"),
    ("Emergency meeting prep with CEO", "high", "Work"),
    ("Finalize contract with vendor today", "high", "Work"),
    ("Release hotfix to production", "high", "Work"),
    # Work - medium
    ("Weekly team sync on Zoom", "medium", "Work"),
    ("Update project documentation", "medium", "Work"),
    ("Code review for PR #234", "medium", "Work"),
    ("Plan next sprint backlog", "medium", "Work"),
    ("Email follow-up with marketing team", "medium", "Work"),
    ("Organize desk and files", "medium", "Work"),
    ("Schedule 1:1 with manager", "medium", "Work"),
    ("Write meeting notes from standup", "medium", "Work"),
    ("Test new feature on staging", "medium", "Work"),
    ("Draft Q2 goals", "medium", "Work"),
    # Work - low
    ("Optional: read industry newsletter", "low", "Work"),
    ("Someday: update LinkedIn profile", "low", "Work"),
    ("Maybe: explore new tool", "low", "Work"),
    # Personal - high
    ("Pick up kids from school at 3pm", "high", "Personal"),
    ("Pay rent today", "high", "Personal"),
    ("Vet appointment for dog tomorrow", "high", "Personal"),
    ("Renew passport before trip", "high", "Personal"),
    # Personal - medium
    ("Buy groceries", "medium", "Personal"),
    ("Call mom this weekend", "medium", "Personal"),
    ("Book haircut", "medium", "Personal"),
    ("Clean the garage", "medium", "Personal"),
    ("Organize closet", "medium", "Personal"),
    ("Plan family dinner", "medium", "Personal"),
    ("Fix leaking tap", "medium", "Personal"),
    ("Return package to post office", "medium", "Personal"),
    ("Water plants", "medium", "Personal"),
    ("Sort mail", "medium", "Personal"),
    # Personal - low
    ("Eventually declutter attic", "low", "Personal"),
    ("Nice to have: new curtains", "low", "Personal"),
    # Health - high
    ("Call dentist for urgent tooth pain", "high", "Health"),
    ("Pick up prescription today", "high", "Health"),
    ("Doctor appointment tomorrow 10am", "high", "Health"),
    ("Take medicine with breakfast", "high", "Health"),
    # Health - medium
    ("Gym workout", "medium", "Health"),
    ("Meal prep for the week", "medium", "Health"),
    ("30 min run", "medium", "Health"),
    ("Yoga session", "medium", "Health"),
    ("Schedule annual checkup", "medium", "Health"),
    ("Drink 8 glasses of water", "medium", "Health"),
    ("Take vitamins", "medium", "Health"),
    ("Evening walk", "medium", "Health"),
    ("Stretch before bed", "medium", "Health"),
    # Health - low
    ("Optional: try new smoothie recipe", "low", "Health"),
    ("Someday: join swimming class", "low", "Health"),
    # Learning - high
    ("Complete certification before expiry", "high", "Learning"),
    ("Study for exam next week", "high", "Learning"),
    ("Finish course project deadline", "high", "Learning"),
    # Learning - medium
    ("Complete Python tutorial", "medium", "Learning"),
    ("Read chapter 5 of textbook", "medium", "Learning"),
    ("Watch webinar on React", "medium", "Learning"),
    ("Practice Spanish 20 min", "medium", "Learning"),
    ("Do coding challenge", "medium", "Learning"),
    ("Take online course module", "medium", "Learning"),
    ("Review lecture notes", "medium", "Learning"),
    ("Research topic for essay", "medium", "Learning"),
    ("Practice presentation", "medium", "Learning"),
    # Learning - low
    ("Eventually read that book", "low", "Learning"),
    ("Maybe learn guitar", "low", "Learning"),
    # Finance - high
    ("Pay electricity bill before disconnect", "high", "Finance"),
    ("File taxes by deadline", "high", "Finance"),
    ("Urgent: fix overdraft", "high", "Finance"),
    # Finance - medium
    ("Submit expenses", "medium", "Finance"),
    ("Review monthly budget", "medium", "Finance"),
    ("Transfer money to savings", "medium", "Finance"),
    ("Cancel unused subscription", "medium", "Finance"),
    ("Update budget spreadsheet", "medium", "Finance"),
    ("Check bank statement", "medium", "Finance"),
    ("Pay credit card", "medium", "Finance"),
    ("Invoice client for project", "medium", "Finance"),
    # Finance - low
    ("Someday: look into investments", "low", "Finance"),
    # Other
    ("Vote in local election", "high", "Other"),
    ("Renew car registration", "medium", "Other"),
    ("Donate old clothes", "low", "Other"),
    ("Call plumber for quote", "medium", "Other"),
    ("Plan vacation", "low", "Other"),
]

def main():
    rows = [("text", "priority", "category")]
    target = 500
    while len(rows) - 1 < target:
        text, prio, cat = random.choice(TASKS)
        # Slight variation: add optional prefix/suffix sometimes
        if random.random() < 0.15:
            text = "Reminder: " + text
        elif random.random() < 0.1:
            text = text + " (important)"
        rows.append((text, prio, cat))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerows(rows)
    print(f"Wrote {len(rows)-1} rows to {OUT}")

if __name__ == "__main__":
    main()
