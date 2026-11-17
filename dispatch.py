"""
Hostel Maintenance Demand Triage & Technician Dispatch Tool
Target User: Hostel Supervisor ( Mr. Manoj Kumar)
Dataset: data.csv (Transcribed from active hostel physical complaint registers)
"""

import csv
import sys
import os
import re
import argparse
from datetime import datetime
from collections import defaultdict

# ==============================================================================
# CONFIGURABLE THRESHOLDS (Easily modified for live testing / operational tuning)
# ==============================================================================
DEFAULT_ACCUMULATION_THRESHOLD = 4   # Minimum unresolved complaints to justify calling a contractor
DEFAULT_AVG_JOB_MINUTES = 25        # Estimated minutes per repair visit
DEFAULT_VISIT_HOURS = 2.0           # Standard technician shift duration (hours)
CRITICAL_KEYWORDS = [
    "sparking", "darkness", "no power", "socket problem", 
    "flickering", "smell", "leak", "flush", "lock broken", "broken lock"
]

def parse_room_details(room_raw):
    """
    Normalizes messy real-world room strings from the physical register into 
    (block, floor, clean_room_id).
    Examples handled:
      'D308'           -> ('D', 3, 'D308')
      'B008'           -> ('B', 0, 'B008')
      'E Block 6th'    -> ('E', 6, 'E-Floor6')
      'F-Block F-018'  -> ('F', 0, 'F018')
      '6th floor D Block' -> ('D', 6, 'D-Floor6')
      'C-608'          -> ('C', 6, 'C608')
    """
    raw = str(room_raw).strip()
    if not raw:
        return ("Unknown", 99, "Unassigned")
    
    # Check for formats like "6th floor D Block" or "5th floor D Block"
    m_floor_block = re.search(r'(\d+)(?:st|nd|rd|th)?\s*floor\s*([A-Fa-f])\s*block', raw, re.IGNORECASE)
    if m_floor_block:
        floor = int(m_floor_block.group(1))
        block = m_floor_block.group(2).upper()
        return (block, floor, f"{block}-Floor{floor}")

    # Check for formats like "E Block 6th"
    m_block_floor = re.search(r'([A-Fa-f])\s*block\s*(\d+)(?:st|nd|rd|th)?', raw, re.IGNORECASE)
    if m_block_floor:
        block = m_block_floor.group(1).upper()
        floor = int(m_block_floor.group(2))
        return (block, floor, f"{block}-Floor{floor}")

    # Check for formats like "F-Block Ground"
    if "ground" in raw.lower():
        m_block = re.search(r'([A-Fa-f])', raw)
        block = m_block.group(1).upper() if m_block else "Unknown"
        return (block, 0, f"{block}-Ground")

    # Standard formats: D308, C-608, F415, B008, A-403
    m_std = re.search(r'([A-Fa-f])[-_\s]*(\d{1,4})', raw)
    if m_std:
        block = m_std.group(1).upper()
        digits = m_std.group(2)
        if len(digits) == 3:
            floor = int(digits[0])
        elif len(digits) == 4:
            floor = int(digits[:2]) if int(digits[:2]) < 10 else int(digits[0])
        elif len(digits) == 1:
            floor = 0
        else:
            floor = 0
        return (block, floor, f"{block}{digits}")

    return ("Other", 99, raw)

def parse_date_flexibly(date_str):
    """Parses various date formats from the register (e.g. 24/7/25, 08-08-2026, 29-01-26)."""
    raw = str(date_str).strip()
    if not raw:
        return None
    for fmt in ("%d/%m/%y", "%d/%m/%Y", "%d-%m-%Y", "%d-%m-%y", "%d/%m/%y", "%d-%m/%y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass
    return None

def load_complaints(csv_path):
    """Loads and standardizes complaints from data.csv."""
    if not os.path.exists(csv_path):
        print(f"Error: Could not find '{csv_path}'. Make sure data.csv is in the working directory.")
        sys.exit(1)
        
    complaints = []
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row.get("complaint_id", "").strip()
            date_raw = row.get("complaint_date", "").strip()
            room_raw = row.get("room_number", "").strip()
            dept_raw = row.get("department", "").strip()
            desc = row.get("complaint_description", "").strip()
            reported_time = row.get("reported_time", "").strip()
            action_taken = row.get("action_taken", "").strip()
            status = row.get("status", "Unknown").strip()

            # Skip empty or header rows
            if not cid and not desc:
                continue

            block, floor, clean_room = parse_room_details(room_raw)
            dt = parse_date_flexibly(date_raw)

            # Detect urgency based on keywords
            is_urgent = any(kw in desc.lower() for kw in CRITICAL_KEYWORDS)
            urgency = "HIGH" if is_urgent else "NORMAL"

            complaints.append({
                "id": cid,
                "date_raw": date_raw,
                "date": dt,
                "room_raw": room_raw,
                "clean_room": clean_room,
                "block": block,
                "floor": floor,
                "department": dept_raw,
                "description": desc,
                "reported_time": reported_time,
                "action_taken": action_taken,
                "status": status,
                "urgency": urgency
            })
    return complaints

def matches_department(dept_raw, target_dept):
    """Matches single or multi-trade entries (e.g. 'Carpentry/Electrical')."""
    if target_dept.lower() == "all":
        return True
    
    mapping = {
        "electrical": ["electric", "light", "fan", "plug", "socket", "regulator"],
        "plumbing": ["plumb", "tap", "leak", "basin", "geyser", "shower", "flush"],
        "carpentry": ["carpent", "cupboard", "door", "table", "chair", "bed", "drawer", "lock"],
        "civil": ["civil", "sanitary", "clean", "washroom", "toilet", "bathroom"]
    }
    
    target_key = target_dept.lower()
    keywords = mapping.get(target_key, [target_key])
    
    combined_text = dept_raw.lower()
    return any(k in combined_text for k in keywords)

def generate_dispatch_manifest(csv_path="data.csv", target_dept="Electrical", 
                               threshold=DEFAULT_ACCUMULATION_THRESHOLD, 
                               hours=DEFAULT_VISIT_HOURS, 
                               avg_job_mins=DEFAULT_AVG_JOB_MINUTES,
                               block_filter=None):
    """
    Main dispatch engine:
    1. Filters complaints by department.
    2. Evaluates accumulation threshold.
    3. Batches visits by Block and Floor to avoid stair backtracking.
    4. Constrains output to technician time capacity.
    5. Formats WhatsApp announcement text.
    """
    all_complaints = load_complaints(csv_path)

    # Department backlog overview across all trades
    trade_counts = defaultdict(int)
    for c in all_complaints:
        dept = c["department"]
        if "elect" in dept.lower():
            trade_counts["Electrical"] += 1
        if "carpent" in dept.lower():
            trade_counts["Carpentry"] += 1
        if "plumb" in dept.lower():
            trade_counts["Plumbing"] += 1
        if "civil" in dept.lower() or "sanitary" in dept.lower():
            trade_counts["Civil/Sanitary"] += 1

    # Filter target complaints
    filtered = [c for c in all_complaints if matches_department(c["department"], target_dept)]
    if block_filter:
        filtered = [c for c in filtered if c["block"].upper() == block_filter.upper()]

    total_open = len(filtered)
    high_urgency_count = sum(1 for c in filtered if c["urgency"] == "HIGH")

    # Time capacity calculation
    total_minutes = int(hours * 60)
    max_rooms = max(1, total_minutes // avg_job_mins)

    # Group by Room to deduplicate repeated complaints
    rooms_map = defaultdict(list)
    for c in filtered:
        rooms_map[c["clean_room"]].append(c)

    # Sort rooms: High urgency first, then by Block, then by Floor ascending (Ground -> 1 -> 2 -> 3)
    def room_sort_key(item):
        room_id, comp_list = item
        block = comp_list[0]["block"]
        floor = comp_list[0]["floor"]
        has_high_urgency = any(c["urgency"] == "HIGH" for c in comp_list)
        # Urgency rank (0 if high, 1 if normal), then block, then floor, then room_id
        return (0 if has_high_urgency else 1, block, floor, room_id)

    sorted_rooms = sorted(rooms_map.items(), key=room_sort_key)
    scheduled_rooms = sorted_rooms[:max_rooms]
    overflow_rooms = sorted_rooms[max_rooms:]

    # Build output report
    print("=" * 72)
    print("      HOSTEL MAINTENANCE TRIAGE & TECHNICIAN DISPATCH MANIFEST      ")
    print("=" * 72)
    print(f"Target Department : {target_dept.upper()}")
    print(f"Shift Duration    : {hours} Hours ({total_minutes} mins available, ~{avg_job_mins} mins/repair)")
    print(f"Current Backlog   : {total_open} recorded complaints across {len(rooms_map)} distinct rooms")
    print(f"Active Threshold  : {threshold} complaints minimum required to summon external contractor")
    print("-" * 72)

    # 1. THRESHOLD EVALUATION
    threshold_met = (total_open >= threshold) or (high_urgency_count > 0)
    print("[THRESHOLD EVALUATION]")
    if total_open >= threshold:
        print(f"  [STATUS: DISPATCH TRIGGERED] -> Backlog count ({total_open}) meets accumulation quota ({threshold}).")
        print(f"  Action: Call contractor for {target_dept} visit.")
    elif high_urgency_count > 0:
        print(f"  [STATUS: DISPATCH TRIGGERED] -> {high_urgency_count} CRITICAL issue(s) detected. Overrides accumulation threshold.")
        print(f"  Action: Call contractor immediately due to safety/functional urgency.")
    else:
        print(f"  [STATUS: ACCUMULATING] -> Backlog count ({total_open}) is below quota ({threshold}).")
        print(f"  Action: Hold off on calling contractor until more complaints accumulate.")
    print("-" * 72)

    # 2. OVERALL HOSTEL BACKLOG SUMMARY
    print("[CAMPUS-WIDE BACKLOG SNAPSHOT]")
    for trade, cnt in sorted(trade_counts.items(), key=lambda x: x[1], reverse=True):
        status_tag = "READY TO CALL" if cnt >= threshold else "ACCUMULATING"
        print(f"  * {trade:<16}: {cnt:>2} complaints [{status_tag}]")
    print("-" * 72)

    # 3. FLOOR-BATCHED TECHNICIAN MANIFEST
    print(f"[TECHNICIAN JOB CARD: {target_dept.upper()}] (Batched by Floor to eliminate vertical backtracking)")
    if not scheduled_rooms:
        print("  No complaints recorded for this trade.")
    else:
        current_block_floor = None
        for i, (room_id, comp_list) in enumerate(scheduled_rooms, 1):
            block = comp_list[0]["block"]
            floor = comp_list[0]["floor"]
            block_floor_header = f"Block {block} - Floor {floor if floor < 99 else 'Unassigned'}"
            
            if block_floor_header != current_block_floor:
                current_block_floor = block_floor_header
                print(f"\n  -- {current_block_floor} --")
            
            has_urgent = any(c["urgency"] == "HIGH" for c in comp_list)
            urgency_flag = "[HIGH PRIORITY]" if has_urgent else "[NORMAL]"
            timing_notes = [c["reported_time"] for c in comp_list if c["reported_time"]]
            timing_str = f" | Pref Time: {', '.join(timing_notes)}" if timing_notes else ""

            # Check for multiple logs (duplicates)
            multi_note = f" (DUPLICATE LOGGED {len(comp_list)}x)" if len(comp_list) > 1 else ""
            print(f"  {i}. Room {room_id:<8} {urgency_flag}{multi_note}{timing_str}")
            
            for c in comp_list:
                print(f"     -> [{c['id']}] {c['description']} (Logged: {c['date_raw']})")

    # 4. OVERFLOW ROOMS (Deferred to next shift)
    if overflow_rooms:
        print(f"\n[DEFERRED / NEXT BATCH] ({len(overflow_rooms)} rooms exceeding {hours}-hour capacity):")
        for room_id, comp_list in overflow_rooms:
            print(f"  * Room {room_id} ({len(comp_list)} issue{'s' if len(comp_list)>1 else ''}) - deferred to next shift")
    print("-" * 72)

    # 5. WHATSAPP BROADCAST NOTICE GENERATOR
    room_list_str = ", ".join(r[0] for r in scheduled_rooms)
    print("[WHATSAPP BROADCAST NOTICE] (Ready to copy-paste into Hostel Group):")
    print('"""')
    print(f"NOTICE: {target_dept.upper()} MAINTENANCE VISIT SCHEDULED")
    print(f"Technician shift window: {hours} hours (Approx. {datetime.now().strftime('%I:%M %p')})")
    print(f"Scheduled Rooms ({len(scheduled_rooms)} rooms):")
    print(f"{room_list_str}")
    print("Important: Please ensure someone is in the room. If unavailable, coordinate with your room neighbor.")
    print('"""')
    print("=" * 72)

def main():
    parser = argparse.ArgumentParser(description="Hostel Maintenance Demand Triage & Technician Dispatch Tool")
    parser.add_argument("--csv", default="data.csv", help="Path to data.csv (default: data.csv)")
    parser.add_argument("--department", "-d", default="Electrical", help="Target department: Electrical, Carpentry, Plumbing, Civil (default: Electrical)")
    parser.add_argument("--threshold", "-t", type=int, default=DEFAULT_ACCUMULATION_THRESHOLD, help=f"Accumulation threshold (default: {DEFAULT_ACCUMULATION_THRESHOLD})")
    parser.add_argument("--hours", "-H", type=float, default=DEFAULT_VISIT_HOURS, help=f"Technician visit duration in hours (default: {DEFAULT_VISIT_HOURS})")
    parser.add_argument("--repair-mins", "-m", type=int, default=DEFAULT_AVG_JOB_MINUTES, help=f"Average minutes per room repair (default: {DEFAULT_AVG_JOB_MINUTES})")
    parser.add_argument("--block", "-b", default=None, help="Filter by specific hostel block (e.g., A, B, C, D, E, F)")
    
    args = parser.parse_args()
    generate_dispatch_manifest(
        csv_path=args.csv,
        target_dept=args.department,
        threshold=args.threshold,
        hours=args.hours,
        avg_job_mins=args.repair_mins,
        block_filter=args.block
    )

if __name__ == "__main__":
    main()
