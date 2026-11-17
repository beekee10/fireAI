# chat-gpt Development Chat Log

### Turn 0: Initial Brainstorming & Problem Definition (ChatGPT)

**Prompt:**
> For Phase 1, I want to add some points to structure my problem statement:
> 1. The register is near the guard room which is 100m from the hostel.
> 2. There are multiple registers for different departments.
> 3. Students sometimes write their complaint and sometimes they forget.
> 4. Electricians or plumbers only visit the hostel sometimes, and when they come, students are often not present.
> 5. Students also tell the supervisor by call or message, but he can forget about this.
> 
> Can you format this into a structured problem statement for my research?

**ChatGPT:**
> **Problem Statement: Hostel Maintenance Management**
> 
> In my hostel, students report maintenance complaints through physical registers, phone calls, and messages.
> 
> The physical complaint register is located near the guard room, approximately 100 metres from the hostel.
> 
> Different maintenance departments maintain separate registers, making complaint records fragmented.
> 
> Some students forget to register their complaints, while complaints communicated through calls or messages may also be forgotten by the supervisor.
> 
> Additionally, electricians and plumbers visit periodically, but students are sometimes unavailable when maintenance staff arrive, creating coordination difficulties.

---


**Prompt:**
> Looking at the data, some rooms have multiple complaints for the exact same problem. For example, Room `E303` has three complaints for a broken door handle (`C019`, `C022`, `C023`), and Room `B008` has two. Also, technicians usually only stay for 2 or 3 hours. How should the script handle duplicates and time limits?

**ChatGPT:**
> We should group complaints by `clean_room` using a dictionary before sorting:
> 1. **Deduplication:** When grouping by room, if a room has multiple entries, we combine them into a single visit item and tag it with `(DUPLICATE LOGGED 2x)` so the technician knows multiple students reported the same issue.
> 2. **Shift Capacity Calculation:** We can take the technician's available hours (e.g., `--hours 2.0`) and an average repair estimate (`DEFAULT_AVG_JOB_MINUTES = 25`). A 2-hour window gives `120 // 25 = 4` rooms maximum.
> 3. **Overflow Handling:** The script schedules the top 4 rooms that fit the window, and lists the rest under a `[DEFERRED / NEXT BATCH]` section so unaddressed complaints aren't lost.

---



**Prompt:**
> The physical register doesn't have a priority column. How can the script identify which complaints are urgent so they get scheduled first?

**ChatGPT:**
> We can implement a keyword-based heuristic check on `complaint_description`. We define a list of safety and functional critical keywords:
> `["sparking", "darkness", "no power", "socket problem", "flickering", "leak", "flush", "lock broken"]`
> 
> - If any keyword appears (e.g., `C029: "...Darkness"` or `C039: "...flickering"`), the complaint is flagged as `HIGH`.
> - In our sorting key, `HIGH` priority rooms are assigned rank 0 and normal complaints rank 1, so urgent issues are placed at the front of the route.
> - Furthermore, if even one `HIGH` issue exists, it overrides the accumulation threshold to trigger an immediate call.

---



**Prompt:**
> The caretaker said students are often away in class when workers arrive. Since we aren't building a student app, how do we solve the locked room problem.can we use whatsapp in this ?

**ChatGPT:**
> At the end of the script execution, the tool formats a ready-to-copy WhatsApp broadcast message:
> ```text
> NOTICE: ELECTRICAL MAINTENANCE VISIT SCHEDULED
> Technician shift window: 2.0 hours
> Scheduled Rooms: D204, D416, F-Ground, F405
> Important: Please ensure someone is in the room. If unavailable, coordinate with your room neighbor.
> ```
> The caretaker can copy-paste this into the official hostel WhatsApp group with one click. Students know exactly when to expect the technician without installing any app.

---


