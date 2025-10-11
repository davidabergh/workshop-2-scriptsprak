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

report += "Total cost of all incidents: " + f"{total_cost:,.2f}".replace(",", " ").replace(".", ",") + " SEK\n\n"

report += "AVERAGE RESOLUTION TIME PER SEVERITY\n-------------------------------------\n"

# Creating a structure to sum up times per severity
severity_times = {}
severity_counts = {}

#Picked r in variable cause it's easier
for r in incidents: 
    sev = (r.get("severity") or "").strip().lower()
    time_str = r.get("resolution_minutes", "")
    if sev and time_str.isdigit():
        severity_times[sev] = severity_times.get(sev, 0) + int(time_str)
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

for sev in ["critical", "high", "medium", "low"]:
    total = severity_times.get(sev, 0)
    count = severity_counts.get(sev, 0)
    if count:
        avg = total / count
        report += f"{sev.title():<10}: {avg:.1f} min\n\n" #average handling time in minutes rounded to 1 decimal
    else:
        report += f"{sev.title():<10}: -\n"

report += "SUMMARY BY SITE\n----------------\n"

#Making a counter to sum up the sites
site_stats = {}

for r in incidents:  
    site = (r.get("site") or "Okänd").strip()

    if "_cost" in r:
        cost = float(r["_cost"])
    else:
        cs = (r.get("cost_sek") or "").replace(" ", "").replace(",", ".")
        cost = float(cs) if cs else 0.0

    # minuter (heltal), 0 om tomt/ogiltigt
    mins_str = (r.get("resolution_minutes") or "").strip()
    mins = int(mins_str) if mins_str.isdigit() else 0

    if site not in site_stats:
        site_stats[site] = {"count": 0, "cost": 0.0, "mins": 0}
    site_stats[site]["count"] += 1
    site_stats[site]["cost"]  += cost
    site_stats[site]["mins"]  += mins

# sorted out, swedish format
report += f"{'Site':<18}{'Incidents':>10}{'Totalkostnad':>18}{'Snitt min':>12}\n"

def fmt_sek(x: float) -> str:
    # 12345.67 into swedish format "12 345,67"

    return f"{x:,.2f}".replace(",", " ").replace(".", ",")
for site in sorted(site_stats):
    c   = site_stats[site]["count"]
    tot = site_stats[site]["cost"]
    m   = site_stats[site]["mins"]
    avg = (m / c) if c else 0.0
    report += f"{site:<18}{c:>10}{fmt_sek(tot):>18} {avg:>11.1f}\n\n"

report += "INCIDENTS PER CATEGORY (AVERAGE IMPACT)\n-----------------------------------------\n"

cat_scores = {}
cat_counts = {}

# Getting the categories and the impact score

for r in incidents:
    cat = (r.get("category") or "Okänd").strip()
    score_str = (r.get("impact_score") or "").strip()
    
# Calculating average impact score, parsing scores to numbers
    if score_str:
        try:
            score = float(score_str)
        except ValueError:
            score = 0.0
    else:
        score = 0.0

# accumulating scores per category
    cat_scores[cat] = cat_scores.get(cat, 0.0) + score
    cat_counts[cat] = cat_counts.get(cat, 0) + 1


for cat in sorted(cat_scores):
    avg = cat_scores[cat] / cat_counts[cat] if cat_counts[cat] else 0.0 #the average score
    report += f"{cat:<20} {avg:>6.2f}\n"

#We are importing the following write script to our csv file incidents_by_site.sv

from csv_out import write_incidents_by_site #csv_out is our 


# write_incidents_by_site(...) is our function and the file for it is csv_out
write_incidents_by_site(incidents, "incidents_by_site.csv")






with open('incident_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(report)