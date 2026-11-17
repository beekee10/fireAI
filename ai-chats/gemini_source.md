# AI Interaction Log: Gemini Vision OCR Extraction

**Prompt to Gemini:**
> Extract the text from the uploaded images and arrange them in a data.csv file containing all the text and contents present in the images. And also arrange the text:
> `complaint_id,complaint_date,room_number,department,complaint_description,reported_time,action_taken,remarks,status`

**Uploaded Images:** 
Photographs of active physical complaint registers taken at the hostel entrance guard desk.

**Gemini Output Sample (First 25 Extracted Rows):**

```csv
complaint_id,complaint_date,room_number,department,complaint_description,reported_time,action_taken,remarks,status
C001,23/2/25,D308,Civil/Sanitary,Bathroom & Toilet & Corridor Not Clean,[unclear],3rd floor - D,[unclear],Unknown
C002,24/7/25,B604,Civil/Sanitary,Clean Bathroom Toilet,[unclear],6th floor - B,[unclear],Unknown
C003,24/7/25,F415,Carpentry,Cupboard broken,[unclear],4th floor - F,[unclear],Unknown
C004,25/7/25,F410,Civil/Sanitary,Clean Bathroom & Corridor,[unclear],4th floor - F,[unclear],Unknown
C005,24/7/25,C213,Carpentry,Cupboard broken,[unclear],2nd floor - C,[unclear],Unknown
C006,28/7/25,D606,Carpentry,Door opener,[unclear],6th floor - D,[unclear],Unknown
C007,28/7/25,E507,Plumbing,Basin Tap is not working / Low pressure in Taps,[unclear],5th floor E-Block,[unclear],Unknown
C008,31/07/25,D015,Civil/Sanitary,Clean Bathroom & Toilet / They smell very bad,[unclear],Ground floor D-Block,[unclear],Unknown
C009,31/7/25,B008,Carpentry,Door open problem,[unclear],Ground floor B-block,[unclear],Unknown
C010,31/7/25,B019,Carpentry,Door open problem,[unclear],Ground floor B,[unclear],Unknown
C011,08-08-2026,B309,Electrical,No Main tubelight in room,[unclear],Light not working,[unclear],Unknown
C012,13-08-2026,E613,Electrical,No Fan Regulator,[unclear],,,Unknown
C013,17-08-2026,C612,Electrical,FAN NOT WORKING,[unclear],,,Unknown
C014,18-08-2026,E303,Carpentry,Door handle / Bathroom cleaning (blockage),,[unclear],Unknown
C015,19-08-2026,E411,Electrical,FAN NOT WORKING,[unclear],,,Unknown
C016,19-08-2026,F215,Carpentry,Desk Drawer broken,[unclear],,,Unknown
C017,23-08-2026,E303,Carpentry,Door handle broken,[unclear],,,Unknown
C018,27-08-2026,D101,Carpentry,Door handle (carpenter),,[unclear],Unknown
C019,11-09-2026,F216,Electrical,FAN - ISSUE,[unclear],,,Unknown
C020,27-08-2025,A109,Carpentry,Door handle missing,[unclear],,,Unknown
C021,29-01-2026,E Block 6th,Plumbing,Flush not working & dustbin missing,[unclear],,,Unknown
C022,29-01-2026,F Block Ground,Electrical,Inside my room electricity not working (bulb & fan not working),,,Unknown
C023,31-01-2026,F-607,Civil/Carpentry,Washroom cleaning, socket problem and room door broken,[unclear],For cleaning washroom socket problem and room door broken,Unknown
C024,13-02-2026,C-608,Electrical,Fan speed is very slow,[unclear],Fan speed is very slow,Unknown
C025,07-08-2026,6th floor D,Civil/Sanitary,Bathroom has not been cleaned from 10 days,[unclear],,,Unknown
```

**Post-Processing Note:**
The raw OCR output contained some `[unclear]` markings in the reported time and remarks columns due to faint pencil or cursive handwriting in the ledger. Subsequent transcription and cleaning was performed to expand the dataset to 74 verified entries in `data.csv`.
