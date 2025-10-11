
import csv

def write_incidents_by_site(incidents, out_path="incidents_by_site.csv"):
    site_stats = {}
    for r in incidents:
        site = (r.get("site") or "Okänd").strip()
        cs = (r.get("cost_sek") or "").replace(" ", "").replace(",", ".") # Float for swedish cost of course
        cost = float(cs) if cs else float(r.get("_cost", 0.0))
        mins_s = (r.get("resolution_minutes") or "").strip() # Counted resolution minutes
        mins = int(mins_s) if mins_s.isdigit() else 0

        s = site_stats.setdefault(site, {"count": 0, "cost": 0.0, "mins": 0})
        s["count"] += 1; s["cost"] += cost; s["mins"] += mins

    with open(out_path, "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["site","total_incidents","total_cost_sek","avg_resolution_minutes"])
        w.writeheader()
        for site, s in sorted(site_stats.items()):  # Alphabetical order per site printed
            c = s["count"]                          # C is variable for number of incidents
            avg = (s["mins"] / c) if c else 0.0
            w.writerow({
                "site": site,
                "total_incidents": c,
                "total_cost_sek": f"{s['cost']:.2f}", # I tried using 2 decimals here
                "avg_resolution_minutes": f"{avg:.1f}",
            })

