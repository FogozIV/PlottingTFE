import numpy as np
import matplotlib.pyplot as plt

# Common settings for visibility
TITLE_FONTSIZE = 26
LABEL_FONTSIZE = 20
TICK_FONTSIZE = 18
LEGEND_FONTSIZE = 18
LINEWIDTH = 3.0
GRID_LINEWIDTH = 1.2

# Base signal setup
frequency = 0.2
duration = 10
sampling_rate = 100
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# ----- Error signal A: product of sines/cos -----
error_a = 5 * np.sin(2 * np.pi * 0.2 * t) * np.sin(2 * np.pi * 0.5 * t) * np.cos(2 * np.pi * 0.15 * t)

# Integrals for A
ise_a = np.cumsum(error_a**2) / sampling_rate
iae_a = np.cumsum(np.abs(error_a)) / sampling_rate
itae_a = np.cumsum(t * np.abs(error_a)) / sampling_rate
itse_a = np.cumsum(t * error_a**2) / sampling_rate

# ----- Error signal B: single sine -----
error_b = 5 * np.sin(2 * np.pi * 0.2 * t)

# Integrals for B
ise_b = np.cumsum(error_b**2) / sampling_rate
iae_b = np.cumsum(np.abs(error_b)) / sampling_rate
itae_b = np.cumsum(t * np.abs(error_b)) / sampling_rate
itse_b = np.cumsum(t * error_b**2) / sampling_rate

# ---------- Plot 1: Error signal A ----------
plt.figure(figsize=(13, 5))
plt.plot(t, error_a, linewidth=LINEWIDTH, label="Error signal")
plt.xlabel("Time (s)", fontsize=LABEL_FONTSIZE)
plt.ylabel("Error", fontsize=LABEL_FONTSIZE)
plt.title(r"Error signal: $e(t)=5\sin(2\pi\cdot0.2t)\sin(2\pi\cdot0.5t)\cos(2\pi\cdot0.15t)$", fontsize=TITLE_FONTSIZE)
plt.grid(True, linewidth=GRID_LINEWIDTH)
plt.tick_params(axis='both', labelsize=TICK_FONTSIZE)
plt.legend(fontsize=LEGEND_FONTSIZE)
plt.tight_layout()
plt.show()

# ---------- Plot 2: Comparison indices for A ----------
plt.figure(figsize=(13, 7))
plt.plot(t, ise_a, linewidth=LINEWIDTH, label="ISE")
plt.plot(t, iae_a, linewidth=LINEWIDTH, label="IAE")
plt.plot(t, itae_a, linewidth=LINEWIDTH, label="ITAE")
plt.plot(t, itse_a, linewidth=LINEWIDTH, label="ITSE")
plt.xlabel("Time (s)", fontsize=LABEL_FONTSIZE)
plt.ylabel("Value", fontsize=LABEL_FONTSIZE)
plt.title("Comparison of Error Performance Indices (Product signal)", fontsize=TITLE_FONTSIZE)
plt.grid(True, linewidth=GRID_LINEWIDTH)
plt.tick_params(axis='both', labelsize=TICK_FONTSIZE)
plt.legend(fontsize=LEGEND_FONTSIZE, ncol=2)
plt.tight_layout()
plt.show()

# ---------- Plot 3: Error signal B ----------
plt.figure(figsize=(13, 5))
plt.plot(t, error_b, linewidth=LINEWIDTH, label="Error signal")
plt.xlabel("Time (s)", fontsize=LABEL_FONTSIZE)
plt.ylabel("Error", fontsize=LABEL_FONTSIZE)
plt.title(r"Error signal: $e(t)=5\sin(2\pi\cdot0.2t)$", fontsize=TITLE_FONTSIZE)
plt.grid(True, linewidth=GRID_LINEWIDTH)
plt.tick_params(axis='both', labelsize=TICK_FONTSIZE)
plt.legend(fontsize=LEGEND_FONTSIZE)
plt.tight_layout()
plt.show()

# ---------- Plot 4: Comparison indices for B ----------
plt.figure(figsize=(13, 7))
plt.plot(t, ise_b, linewidth=LINEWIDTH, label="ISE")
plt.plot(t, iae_b, linewidth=LINEWIDTH, label="IAE")
plt.plot(t, itae_b, linewidth=LINEWIDTH, label="ITAE")
plt.plot(t, itse_b, linewidth=LINEWIDTH, label="ITSE")
plt.xlabel("Time (s)", fontsize=LABEL_FONTSIZE)
plt.ylabel("Value", fontsize=LABEL_FONTSIZE)
plt.title("Comparison of Error Performance Indices (Single sine)", fontsize=TITLE_FONTSIZE)
plt.grid(True, linewidth=GRID_LINEWIDTH)
plt.tick_params(axis='both', labelsize=TICK_FONTSIZE)
plt.legend(fontsize=LEGEND_FONTSIZE, ncol=2)
plt.tight_layout()
plt.show()
