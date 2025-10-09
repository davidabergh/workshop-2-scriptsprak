import csv

# Open the CSV and load all rows as a list of dictionaries (one dict per row), using UTF-8.

with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = list(csv.DictReader(f))



report = "INCIDENT ANALYSIS - SEPTEMBER 2024\n\n"
report +="Analysperiod: 2024-09-01 till 2024-09-30\n\n"

# Showing off the sites sorted in one row
sites = sorted({ (reader.get("site") or "").strip() for reader in incidents if reader.get("site") })
sites_str = ", ".join(sites) if sites else "Okänt"

report += f"Kontor: {sites_str}\n"

report += "\n"

report += "INCIDENTS PER SEVERITY\n-----------------------\n"

# Loop for counting all the incidents per severity

counts = {}
for reader in incidents:
    sev = (reader.get("severity") or "")
    if not sev:
        continue
    counts[sev] = counts.get(sev, 0) + 1

    # Printed out per categories 

for sev in ["critical", "high", "medium", "low"]:
    report += f"{sev.title():<10}{counts.get(sev, 0)}\n"

report += "\n"

#Writing how many incidents affected more than 100 users

report += "INCIDENTS WITH HIGH USER IMPACT\n--------------------------------"

report += "\n"

high_impact = []

for incident in incidents:
    users = incident.get("affected_users")

    if users and users.isdigit() and int(users) >= 100:
     high_impact.append(incident)
if high_impact:
    for r in high_impact:   
        report += f"{r['site']:15} {r['device_hostname']:20} {r['affected_users']} users\n"
else:
    report += "No high impact areas this time.\n"

report += "\n"

report += "TOP 5 MOST EXPENSIVE INCIDENTS\n--------------------------------\n"

#Counting the 5 most exensive incidents
#First of a helper for the swedish costs 

cost_str = "1 234,50"  
cost_float = float(cost_str.replace(' ', '').replace(',', '.'))

for r in incidents:
    r["_cost"] = float(r["cost_sek"].replace(" ", "").replace(",", ".")) if r["cost_sek"] else 0.0

# The top 5 sorted
top5 = sorted(incidents, key=lambda r: r["_cost"], reverse=True)[:5]

# A summary for the top 5
summary_top5 = [
    {"Ticket": r["ticket_id"], "Site": r["site"], "Enhet": r["device_hostname"],
     "Kostnad_SEK": f"{r['_cost']:,.2f}".replace(",", " ").replace(".", ",")}
    for r in top5
]

for row in summary_top5:
    if row["Enhet"] == "Summa topp 5":
        report += f"{row['Enhet']:<35} {row['Kostnad_SEK']} SEK\n"
    else:
        report += f"{row['Ticket']:>13}  {row['Site']:<14}  {row['Enhet']:<18}  {row['Kostnad_SEK']} SEK\n"
report += "\n"


#Calculated costs of all incidents
total_cost = sum(r["_cost"] for r in incidents)
report += f"Total cost of all incidents: {total_cost:,.2f} SEK\n\n"


with open('incident_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(report)