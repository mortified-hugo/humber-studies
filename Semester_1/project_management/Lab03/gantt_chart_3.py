# gantt_project_phases_inverted_with_deliverables.py
# Adds vertical red deliverable markers (full-height) at the end date of specified tasks.
# Python 3.x, requires: matplotlib, pandas

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
from matplotlib.patches import Patch

# Task data (only IDs matching format P#-T#)
tasks = [
    {"id": "P1-T1", "name": "Stakeholder Interviews", "phase": "Phase 1", "start": "2026-01-05", "end": "2026-01-30"},
    {"id": "P1-T2", "name": "Risk Identification", "phase": "Phase 1", "start": "2026-02-02", "end": "2026-02-27"},
    {"id": "P2-T1", "name": "Drafting AIGB Charter", "phase": "Phase 2", "start": "2026-02-20", "end": "2026-02-27"},
    {"id": "P2-T2", "name": "Define AIGB Scope", "phase": "Phase 2", "start": "2026-03-02", "end": "2026-03-13"},
    {"id": "P2-T3", "name": "Define AIGB Scope", "phase": "Phase 2", "start": "2026-03-16", "end": "2026-04-26"},
    {"id": "P3-T1", "name": "Contractor RFP Evaluation", "phase": "Phase 3", "start": "2026-01-01", "end": "2026-04-17"},
    {"id": "P3-T2", "name": "Contractor Selection", "phase": "Phase 3", "start": "2026-03-02", "end": "2026-03-27"},
    {"id": "P3-T3", "name": "Contractor Onboarding", "phase": "Phase 3", "start": "2026-03-30", "end": "2026-05-29"},
    {"id": "P3-T4", "name": "Contractor Onboarding", "phase": "Phase 3", "start": "2026-04-27", "end": "2026-05-15"},
    {"id": "P4-T1", "name": "C# Filter Development", "phase": "Phase 4", "start": "2026-04-27", "end": "2026-06-19"},
    {"id": "P4-T2", "name": "Co-Pilot UI Configuration", "phase": "Phase 4", "start": "2026-06-22", "end": "2026-07-31"},
    {"id": "P4-T3", "name": "Controlled Deployment - Stage 1", "phase": "Phase 4", "start": "2026-08-03", "end": "2026-08-21"},
    {"id": "P4-T4", "name": "Controlled Deployment - Stag 2", "phase": "Phase 4", "start": "2026-08-24", "end": "2026-09-18"},
    {"id": "P4-T5", "name": "Controlled Deployment - Stag 3", "phase": "Phase 4", "start": "2026-09-21", "end": "2026-10-31"},
    {"id": "P5-T1", "name": "Constant Evaluation of Deliverables", "phase": "Phase 5", "start": "2026-06-01", "end": "2026-12-31"},
    {"id": "P5-T2", "name": "Governance Board Re-evaluation", "phase": "Phase 5", "start": "2026-06-01", "end": "2027-02-01"},
]

phase_colors = {
    "Phase 1": "#E63946",
    "Phase 2": "#F4A261",
    "Phase 3": "#F2C94C",
    "Phase 4": "#56CCF2",
    "Phase 5": "#2B4DE9",
}

# Deliverables mapping: deliverable label -> task id whose end date marks the deliverable
deliverables = {
    "Deliverable 1\nRisk Heatmap": "P1-T2",
    "Deliverable 2\nGovernance Board Setup": "P2-T3",
    "Deliverable 3\nAI Training Material": "P3-T2",
    "Deliverable 4\nPipeline Approval": "P3-T4",
    "Deliverable 5\nC# Prompt Filter": "P4-T1",
    "Deliverable 6\nConfigured Co-Pilot": "P4-T2",
}

# Build DataFrame
df = pd.DataFrame(tasks)
df["start_dt"] = pd.to_datetime(df["start"])
df["end_dt"] = pd.to_datetime(df["end"])
df["duration_days"] = (df["end_dt"] - df["start_dt"]).dt.days

# Order by phase number ascending (P1 top) then by start date
def phase_number(phase_label):
    try:
        return int(phase_label.split()[1])
    except Exception:
        return 999

df = df.sort_values(["phase", "start_dt"], key=lambda col: col.map(lambda v: phase_number(v) if col.name == "phase" else v)).reset_index(drop=True)

# Grouping and y positions so Phase 1 appears at top
df["group_index"] = df.groupby("phase").ngroup()
df = df.sort_values(["group_index", "start_dt", "id"], ascending=[True, True, True]).reset_index(drop=True)
total_rows = len(df)
df["ypos"] = range(total_rows, 0, -1)

# Plot
fig, ax = plt.subplots(figsize=(14, 8))
bar_height = 0.6

for _, row in df.iterrows():
    start = mdates.date2num(row["start_dt"])
    end = mdates.date2num(row["end_dt"])
    width = end - start
    color = phase_colors.get(row["phase"], "#888888")
    ax.barh(row["ypos"], width, left=start, height=bar_height, color=color, edgecolor="k", alpha=0.95, zorder=2)
    ax.text(start + width / 2, row["ypos"], row["id"], va="center", ha="center", color="white", fontsize=9, weight="bold", zorder=3)

# Y-axis labels: only show IDs on ticks
ax.set_yticks(df["ypos"])
ax.set_yticklabels(df["id"])
ax.invert_yaxis()

# Add full-height red deliverable markers at each deliverable end date
ymin, ymax = ax.get_ylim()  # y-limits span top to bottom in axis coordinates
for label, task_id in deliverables.items():
    match = df.loc[df["id"] == task_id]
    if match.empty:
        continue
    deliver_dt = match["end_dt"].iloc[0]
    deliver_num = mdates.date2num(deliver_dt)
    # Draw a semi-transparent red vertical bar that spans the full y-axis
    ax.axvspan(deliver_num - 0.2, deliver_num + 0.2, ymin=0, ymax=1, color="#c62828", alpha=0.25, zorder=1)
    # Draw a stronger red line on top for emphasis
    ax.axvline(deliver_num, color="#b71c1c", linewidth=1.8, zorder=4)
    # Annotate deliverable label just above the x-axis (bottom area)
    ax.text(deliver_num, ymin + 0.5, label, rotation=90, va="bottom", ha="center", color="#8b0000", fontsize=10, weight="bold", zorder=5)

# Format x-axis as dates and align right edge to latest end date
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
start_num = mdates.date2num(df["start_dt"].min())
right_dt = df["end_dt"].max()
right_num = mdates.date2num(right_dt)
ax.set_xlim(left=start_num, right=right_num + 0.5)  # small margin so last bar doesn't touch spine
plt.xticks(rotation=30)

# Legend (one entry per phase)
legend_patches = [Patch(facecolor=col, edgecolor="k", label=ph) for ph, col in phase_colors.items()]
legend_patches.append(Patch(facecolor="#c62828", edgecolor="k", label="Deliverable (end date)"))
ax.legend(handles=legend_patches, loc="upper right", title="Phases / Deliverables")

ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.set_xlabel("Date")
ax.set_title("Project Plan Gantt Chart — Main Tasks (P#-T#) with Deliverable Markers")

plt.tight_layout()
plt.show()
