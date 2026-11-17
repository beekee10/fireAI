# Research: Hostel Maintenance Demand & Dispatch

## 1. Problem Statement
At my  hostel, maintenance complaints are logged across separate physical registers kept at the guard room, 100 metres away.
Because complaints are split across separate registers (plumbing, electrical, carpentry), the supervisor cannot see the total open backlog at a glance.
Maintenance workers visit the hostel at certain times, but their visits are not always properly planned.
Sometimes students are attending classes or are not in their rooms when workers arrive, which makes it difficult for workers to complete the repairs.
Complaints communicated through phone calls or WhatsApp messages are frequently forgotten or buried before ever reaching the physical book.

## 2. Target Person & Context
- **Primary Person:** Mr. Manoj Kumar 
- **Role:** Hostel Supervisor/Caretaker
- **Location:** Supervisor Office, Hostel K, NIT Jamshedpur
- **Why this person:** He is the central coordination node between 600+ students and visiting contractors; when coordination fails, he absorbs the blame from both sides.

## 3. Existing Solutions & Why They Do Not Fit

### Existing Solution 1: Department-Specific Physical Paper Registers at Guard Room
- **How it works:** Students walk 100 metres to the guard desk and write complaints in separate books (Electrical, Plumbing, Carpentry).
- **Why it does not fit the Caretaker:** 
  It provides zero unified visibility. When a technician arrives for an hour, the caretaker must manually flip through dozens of handwritten pages across different books, guess which students are currently in their rooms, and manually organize visits. It cannot automatically sort rooms by floor proximity or highlight duplicate complaints.

### Existing Solution 2: Direct Phone Calls & Messaging (WhatsApp)
- **How it works:** Students call or send photos/messages of broken fixtures directly to the caretaker's personal phone.
- **Why it does not fit the Caretaker:** 
  Incoming messages get buried under personal and administrative chats. There is no structured status tracking, so complaints communicated outside office hours are easily forgotten until an angry student calls back. It also fails to inform students when a technician is actually on-site.

## 4. Proposed Tool
A lightweight Python-based **Maintenance Triage & Dispatch Tool** for the caretaker.
The tool reads transcribed register complaint data (`data.csv`) and:
1. Aggregates open complaints by department against an accumulation threshold to determine when to call external technicians.
2. Generates an optimal floor-batched visit manifest for visiting workers to eliminate backtracking between floors.
3. Automatically formats a ready-to-broadcast WhatsApp announcement for the hostel group to alert students when a technician arrives.

## 5. Research Sources

- **Title:** Guidelines for Students’ Complaints and Redressal Mechanism Institution
- **Institution:** Indian Institute of Technology (IITRAM), Ahmedabad
- **Link:** https://iitram.ac.in/public/upload/20240503_IITRAM_Guidelines%20for%20Complaints%20and%20their%20Redressal%20v1Mechanismv2.pdf
- **Three-line summary:** 
  This source shows that hostel students report maintenance complaints in a physical complaint register kept at the Hostel/Mess office, which is almost identical to your project’s existing system.
  The hostel caretaker checks the maintenance register daily and forwards complaints to separate sections such as civil, water works, electrical, sanitary, and network.
  It confirms that the caretaker must follow up on complaints for early resolution, supporting your idea of a single dashboard showing all pending work.
  It is highly suitable because it describes the exact manual workflow your Python tool would improve: complaint entry, department sorting, caretaker follow-up, and escalation.

### Source 2
- **Title:** Complaints Management Systems
- **Institution:** Tata Institute of Social Sciences (TISS), Mumbai
- **Link:** https://www.tiss.ac.in/uploads/files/Complaints_Management_Systems.pdf
- **Three-line summary:** 
  Identifies resident unavailability and erratic vertical travel across multi-story buildings as primary causes of failed campus maintenance calls. 
  Recommends clustering service tickets by physical proximity (wings and floors) and pre-matching technician arrival with resident availability windows. 
  Emphasizes that computerized dispatch does not require complex ERP portals—simple list optimization provides immediate operational relief.
