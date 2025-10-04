import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Define project start and phases (months relative to project start)
project_start = datetime(2026, 1, 1)  # change if needed

phases = [
    ("Phase 1 - Risk Assessment", 0, 2),         # Months 1-2
    ("Phase 2 - Governance Setup", 1, 4),        # Months 2-4
    ("Phase 3 - Capability Building", 2, 9),     # Months 3-9
    ("Phase 4 - Controlled AI Enablement", 4, 12),# Months 6-12
    ("Phase 5 - Continuous Integration", 6, 18), # Months 6-onwards (drawn to month 18 for visualization)
]

# Helper to convert month offsets to datetime
def month_offset_to_date(start, month_offset):
    # approximate each month as 30 days for simple offsets
    return start + timedelta(days=30 * month_offset)

# Build plotting data
labels = [p[0] for p in phases]
starts = [month_offset_to_date(project_start, p[1]) for p in phases]
ends = [month_offset_to_date(project_start, p[2]) for p in phases]
durations = [(e - s).days for s, e in zip(starts, ends)]

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
y_positions = range(len(phases))

bars = ax.barh(
    y=y_positions,
    width=durations,
    left=starts,
    height=0.6,
    align='center',
    color="#2a79c7",
    edgecolor="#0e395f"
)

# Format y-axis
ax.set_yticks(y_positions)
ax.set_yticklabels(labels, fontsize=10)
ax.invert_yaxis()

# Format x-axis as months
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)

# Add grid, title and labels
ax.grid(axis='x', linestyle='--', alpha=0.4)
ax.set_title("Manista Care AI Implementation - Gantt Chart", fontsize=12, weight='bold')
ax.set_xlabel("Timeline")

# Annotate bars with start and end month
for bar, start, end in zip(bars, starts, ends):
    sx = mdates.date2num(start)
    ex = mdates.date2num(end)
    # ax.text(sx + (ex - sx)/2, bar.get_y() + bar.get_height()/2,
    #         f"{start.strftime('%b %Y')} → {end.strftime('%b %Y')}",
    #         ha='center', va='center', color='white', fontsize=9)

plt.tight_layout()
plt.show()
