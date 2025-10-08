import csv

# Open the CSV and load all rows as a list of dictionaries (one dict per row), using UTF-8.

with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = list(csv.DictReader(f))



report = "INCIDENT ANALYSIS - SEPTEMBER 2024\n\n"
report +="Analysperiod: 2024-09-01 till 2024-09-30\n\n"

report += "INCIDENTS PER SEVERITY\n-----------------------\n"

# Loop for counting all the incidents per severity

counts = {}
for r in incidents:
    sev = (r.get("severity") or "").strip().lower()
    if not sev:
        continue
    counts[sev] = counts.get(sev, 0) + 1

    # Printed out per categories 

for sev in ["critical", "high", "medium", "low"]:
    report += f"{sev.title():<10}{counts.get(sev, 0)}\n"

with open('incident_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(report)