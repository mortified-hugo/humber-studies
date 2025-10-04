# gantt_chart.py
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Tasks: (phase, task name, start_week, end_week_inclusive)
tasks = [
    ("Risk Assessment", "P1-T1", 1, 4),
    ("Risk Assessment", "P1-T2", 4, 8),

    ("Governance Board Set Up", "P2-T1", 4, 5),
    ("Governance Board Set Up", "P2-T2", 5, 6),
    ("Governance Board Set Up", "P2-T3", 6, 8),
    ("Governance Board Set Up", "P2-T4", 8, 12),

    ("Capability Building", "P3-T1", 12, 15),
    ("Capability Building", "P3-T3", 15, 16),
    ("Capability Building", "P3-T4", 16, 19),

    ("Controlled Enablement", "P4-T1", 1, 18),  # shown as ongoing until week 18
    ("Controlled Enablement", "P4-T2", 20, 24),
    ("Controlled Enablement", "P4-T3", 24, 28),
    ("Controlled Enablement", "P4-T4", 29, 30),
    ("Controlled Enablement", "P4-T5", 30, 30),
    ("Controlled Enablement", "P4-T6", 31, 34),
]

# Map phases to colors
phase_colors = {
    "Risk Assessment": "#1f77b4",
    "Governance Board Set Up": "#ff7f0e",
    "Capability Building": "#2ca02c",
    "Controlled Enablement": "#d62728",
}

# Prepare plotting positions
labels = []
starts = []
durations = []
colors = []
phases = []

for t in tasks:
    phase, name, start_w, end_w = t
    labels.append(name)
    starts.append(start_w)
    durations.append(max(0.5, end_w - start_w + 1))  # ensure minimum width for single-week tasks
    colors.append(phase_colors.get(phase, "#7f7f7f"))
    phases.append(phase)

# Vertical positions (top to bottom)
y_positions = range(len(labels), 0, -1)

fig, ax = plt.subplots(figsize=(12, max(6, len(labels)*0.35)))

# Draw bars
for y, start, dur, color, label in zip(y_positions, starts, durations, colors, labels):
    ax.barh(y, dur, left=start, height=0.6, align='center', color=color, edgecolor='k')
    ax.text(start + dur/2, y, label, va='center', ha='center', color='white', fontsize=9, weight='bold')

# Axes and grid
ax.set_yticks(list(y_positions))
ax.set_yticklabels([])  # hide default labels because tasks are written on bars
ax.set_xlabel("Project timeline (Weeks)")
ax.set_xlim(0.5, 35)  # show weeks 1..34 plus margin
ax.set_xticks(range(1, 36))
ax.xaxis.grid(True, linestyle='--', alpha=0.5)

# Legend for phases
legend_patches = [mpatches.Patch(color=c, label=p) for p, c in phase_colors.items()]
ax.legend(handles=legend_patches, bbox_to_anchor=(1.02, 1), loc='upper left')

# Title and layout
ax.set_title("Project Gantt Chart (Weeks)")
plt.tight_layout()
plt.show()
