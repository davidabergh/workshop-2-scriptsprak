import csv

with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = list(csv.DictReader(f))

report = "INCIDENT ANALYSIS - SEPTEMBER 2024"

with open('incident_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(report)