# Hostel Maintenance Triage & Technician Dispatch Tool

An operational decision-support and dispatch tool built for the hostel Supervisor to eliminate staircase backtracking, enforce accumulation thresholds for visiting contractors, and generate broadcast notices for students.

- **Primary User:** Hostel Supervisor (Mr. Manoj Kumar)
- **Fieldwork Location:** Supervisor Office, Hostel K, NIT Jamshedpur
- **Fieldwork Date:** November 17, 2026
- **Dataset:** `data.csv` (74 real handwritten entries transcribed from active physical registers)
- **Demo Video (3 minutes):** [ Google Drive Video](https://drive.google.com/file/d/1X1aPQB2-gGnNsYzxNvmWGeOlrrsaK1ov/view) 

## 1. The Real-World Problem

At our hostel complex (Blocks A through F, Ground to 6th floor), students report maintenance issues in paper registers kept at the guard desk.

Through 35 minutes of on-site observation and an in-depth conversation with the hostel supervisor, two critical operational bottlenecks were identified:
1. **The Contractor Accumulation Threshold:** Technicians (electricians, carpenters, plumbers) are outside contractors who charge per visit. The supervisor cannot summon a contractor for a single broken latch or fused bulb; he must wait until **at least 4 complaints accumulate** in that trade to justify the visit cost.
2. **Staircase Backtracking & Locked Rooms:** When contractors arrive for a 2-hour window, complaints in the physical ledger are listed chronologically rather than geographically. Technicians wander randomly between floors (Floor 2 ➔ Floor 6 ➔ Ground floor), wasting up to 30% of their billable window climbing stairs, only to knock on doors where students are away in classes.

---

## 2. What the Tool Does

`dispatch.py` is a zero-dependency Python script that reads the transcribed `data.csv` and produces a single unified dispatch manifest:

1. **Evaluates Contractor Call Thresholds:** Calculates active backlogs across all trades and determines whether a trade has met the accumulation quota (e.g., 4 complaints) or has high-severity safety hazards (e.g., sparking switches, total room darkness) that trigger an immediate visit.
2. **Floor-Batched Route Planning:** Sorts pending repairs by Block and Floor ascending (Ground ➔ Floor 1 ➔ Floor 2...), eliminating vertical backtracking.
3. **Time-Budget Allocation:** Based on the technician's available hours (default: 2.0 hrs) and average repair duration (25 mins/job), it schedules only the rooms that fit into the shift and defers overflow to the next visit.
4. **Deduplication:** Aggregates repeat complaints for the same room (e.g., Room E303 had 3 duplicate complaints for the same broken door handle).
5. **Generates WhatsApp Broadcast Notice:** Formats a ready-to-paste announcement for the hostel WhatsApp group with the scheduled room list so students know when to be present.

---

## 3. How to Run It

### Prerequisites
- Python 3.8+ (Tested on Python 3.14)
- No third-party packages required (uses Python standard libraries: `csv`, `re`, `argparse`, `datetime`).

### Commands

#### Run default dispatch (Electrical, 2-hour shift):
```bash
python dispatch.py
```

#### Run for Carpentry with a 3-hour contractor window:
```bash
python dispatch.py --department carpentry --hours 3
```

#### Run for Plumbing with a custom accumulation threshold (e.g., 2 complaints):
```bash
python dispatch.py --department plumbing --threshold 2 --hours 1.5
```

```

---

## 4. Real Terminal Output

Below is the actual output produced by running `python dispatch.py --department electrical --hours 2`:

```text
========================================================================
      HOSTEL MAINTENANCE TRIAGE & TECHNICIAN DISPATCH MANIFEST      
========================================================================
Target Department : ELECTRICAL
Shift Duration    : 2.0 Hours (120 mins available, ~25 mins/repair)
Current Backlog   : 30 recorded complaints across 30 distinct rooms
Active Threshold  : 4 complaints minimum required to summon external contractor
------------------------------------------------------------------------
[THRESHOLD EVALUATION]
  [STATUS: DISPATCH TRIGGERED] -> Backlog count (30) meets accumulation quota (4).
  Action: Call contractor for Electrical visit.
------------------------------------------------------------------------
[CAMPUS-WIDE BACKLOG SNAPSHOT]
  * Carpentry       : 33 complaints [READY TO CALL]
  * Electrical      : 30 complaints [READY TO CALL]
  * Civil/Sanitary  : 13 complaints [READY TO CALL]
  * Plumbing        :  5 complaints [READY TO CALL]
------------------------------------------------------------------------
[TECHNICIAN JOB CARD: ELECTRICAL] (Batched by Floor to eliminate vertical backtracking)

  -- Block D - Floor 2 --
  1. Room D204     [HIGH PRIORITY]
     -> [C039] Tubelight is flickering. (ii) Intensity is very low. (Logged: 27/7/25)

  -- Block D - Floor 4 --
  2. Room D416     [HIGH PRIORITY]
     -> [C036] Tube light is flickering and intensity is very low (Logged: 27/7/25)

  -- Block F - Floor 0 --
  3. Room F-Ground [HIGH PRIORITY]
     -> [C029] Inside my room electricity not working (like bulb & fan not working) Darkness (Logged: 29-01-26)

  -- Block F - Floor 4 --
  4. Room F405     [HIGH PRIORITY]
     -> [C040] No power Tubelight, fan not working (Logged: 27/7/25)

[DEFERRED / NEXT BATCH] (26 rooms exceeding 2.0-hour capacity):
  * Room F607 (1 issue) - deferred to next shift
  * Room A109 (1 issue) - deferred to next shift
  * Room A403 (1 issue) - deferred to next shift
  * Room A604 (1 issue) - deferred to next shift
  * Room B309 (1 issue) - deferred to next shift
  * Room B511 (1 issue) - deferred to next shift
  * Room C314 (1 issue) - deferred to next shift
  * Room C402 (1 issue) - deferred to next shift
  * Room C408 (1 issue) - deferred to next shift
  * Room C411 (1 issue) - deferred to next shift
  * Room C608 (1 issue) - deferred to next shift
  * Room C612 (1 issue) - deferred to next shift
  * Room D016 (1 issue) - deferred to next shift
  * Room D101 (1 issue) - deferred to next shift
  * Room D203 (1 issue) - deferred to next shift
  * Room D504 (1 issue) - deferred to next shift
  * Room E303 (1 issue) - deferred to next shift
  * Room E317 (1 issue) - deferred to next shift
  * Room E411 (1 issue) - deferred to next shift
  * Room E610 (1 issue) - deferred to next shift
  * Room E613 (1 issue) - deferred to next shift
  * Room F018 (1 issue) - deferred to next shift
  * Room F215 (1 issue) - deferred to next shift
  * Room F216 (1 issue) - deferred to next shift
  * Room F517 (1 issue) - deferred to next shift
  * Room F518 (1 issue) - deferred to next shift
------------------------------------------------------------------------
[WHATSAPP BROADCAST NOTICE] (Ready to copy-paste into Hostel Group):
"""
NOTICE: ELECTRICAL MAINTENANCE VISIT SCHEDULED
Technician shift window: 2.0 hours (Approx. 11:24 PM)
Scheduled Rooms (4 rooms):
D204, D416, F-Ground, F405
Important: Please ensure someone is in the room. If unavailable, coordinate with your room neighbor.
"""
========================================================================
```

---

## 5. What the Tool Gets Wrong (Limitations & Failure Modes)



1. **Student Time-Constraint Conflicts:**
   - *Failure Mode:* In entry `C052`, a student wrote *"Chair & table missing, after 8pm"*. If the carpenter arrives at 2:00 PM, the tool currently schedules room A308 because it matches the floor batch, merely appending `| Pref Time: after 8pm` to the terminal line. It does not automatically demote the room if the shift occurs outside the student's available window.
2. **Multi-Discipline Complaints:**
   - *Failure Mode:* Entry `C050` reads: *"No light in washroom, need 4 tube lights. No Table, No Tubelight. No bulb in room 246"*. This single row requires both an Electrician and a Carpenter. The tool categorizes it under both when searched individually, but cannot coordinate a joint dual-worker visit.
3. **Emergency Hazard Override Dependency:**
   - *Failure Mode:* A critical emergency (e.g., active sparking or water main burst) should bypass the tool entirely. If a student writes a severe hazard into the physical register rather than alerting the guard verbally, relying on batch dispatch could delay emergency response.
4. **Heuristic Room Parsing on Non-Standard Entries:**
   - *Failure Mode:* While regex extracts rooms like `D308` and `C-608`, unusual entries like `C028: "E Block 6th"` or `C034: "6th floor D Block"` do not have room numbers. The tool maps them to floor-level identifiers (`E-Floor6`, `D-Floor6`), requiring the caretaker to ask the guard which exact room on that floor was affected.
