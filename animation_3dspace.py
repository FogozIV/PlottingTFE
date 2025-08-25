# Rolling ball on a (distorted) 3D harmonic potential — configurable view + animation
# You can tweak the parameters in the "CONFIG" section below and re-run the cell.
# The animation will be saved as a GIF you can download.

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)
from matplotlib import animation
import os

# -----------------------------
# CONFIG — tweak these freely
# -----------------------------
# Potential V(x, y) = 1/2 (kx x^2 + ky y^2) + kxy x y
kx = 1.0
ky = 0.25
kxy = 0.0  # try small coupling like 0.15 for a rotated bowl

# Distortion of the vertical axis to "exaggerate" changes
# z = z_scale * sign(V) * |V|**gamma
gamma = 0.6      # < 1 flattens big values, > 1 exaggerates big values
z_scale = 1.0    # overall vertical scaling

# Dynamics (overdamped gradient descent on V)
alpha = 0.12     # mobility (step size multiplier)
dt = 0.05
n_frames = 400

# Initial position of the ball
x0, y0 = 2.0, -1.5

# Plot window for the potential surface
xlim = (-3.5, 3.5)
ylim = (-3.5, 3.5)
grid_n = 120

# View angle (you can change these and re-run)
elev = 35  # elevation in degrees
azim = -60 # azimuth in degrees

# Trail length (in frames); set to 0 to disable
trail_len = 120

# Output file
out_path = "/rolling_ball.gif"
fps = 30

# -----------------------------
# Definitions
# -----------------------------
def V(x, y):
    return 0.5*(kx*x*x + ky*y*y) + kxy*x*y

def gradV(x, y):
    dVdx = kx*x + kxy*y
    dVdy = ky*y + kxy*x
    return dVdx, dVdy

def distort(v):
    # Signed power with overall scale
    return z_scale * np.sign(v) * (np.abs(v) ** gamma + 1e-12)

# Mesh for the surface
xs = np.linspace(xlim[0], xlim[1], grid_n)
ys = np.linspace(ylim[0], ylim[1], grid_n)
X, Y = np.meshgrid(xs, ys)
Z = distort(V(X, Y))

# Simulate trajectory (so we can pre-compute for smooth animation & trail)
xy = np.zeros((n_frames, 2), dtype=float)
x, y = x0, y0
for i in range(n_frames):
    dVdx, dVdy = gradV(x, y)
    x = x - alpha * dVdx * dt
    y = y - alpha * dVdy * dt
    # keep inside bounds a bit (soft clip)
    x = np.clip(x, xlim[0]*0.98, xlim[1]*0.98)
    y = np.clip(y, ylim[0]*0.98, ylim[1]*0.98)
    xy[i] = (x, y)

Z_traj = distort(V(xy[:,0], xy[:,1]))

# -----------------------------
# Figure + Artists
# -----------------------------
fig = plt.figure(figsize=(7.5, 6.5))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=elev, azim=azim)

# Surface
surf = ax.plot_surface(X, Y, Z, rstride=2, cstride=2, linewidth=0, antialiased=True, alpha=0.9)

# Ball (as a point)
(ball_line,) = ax.plot([xy[0,0]], [xy[0,1]], [Z_traj[0]], marker='o', markersize=8, linestyle='')

# Trail
if trail_len > 0:
    (trail_line,) = ax.plot([], [], [], linewidth=2)
else:
    trail_line = None

ax.set_xlim(*xlim)
ax.set_ylim(*ylim)
# Set zlim to include both surface and trajectory for a stable view
Zmin, Zmax = np.min(Z), np.max(Z)
pad = 0.05*(Zmax - Zmin + 1e-12)
ax.set_zlim(Zmin - pad, Zmax + pad)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("distorted V(x, y)")

ax.set_title("Ball rolling on a distorted 3D harmonic potential")

# -----------------------------
# Animation callbacks
# -----------------------------
def init():
    if trail_line is not None:
        trail_line.set_data([], [])
        trail_line.set_3d_properties([])
    ball_line.set_data([xy[0,0]], [xy[0,1]])
    ball_line.set_3d_properties([Z_traj[0]])
    return (ball_line,) if trail_line is None else (ball_line, trail_line)

def update(frame):
    # update ball
    ball_line.set_data([xy[frame,0]], [xy[frame,1]])
    ball_line.set_3d_properties([Z_traj[frame]])
    # update trail
    if trail_line is not None:
        start = max(0, frame - trail_len)
        trail_line.set_data(xy[start:frame+1,0], xy[start:frame+1,1])
        trail_line.set_3d_properties(Z_traj[start:frame+1])
    return (ball_line,) if trail_line is None else (ball_line, trail_line)

anim = animation.FuncAnimation(fig, update, init_func=init, frames=n_frames, interval=1000/fps, blit=True)


def _progress(i, n):
    pct = int((i + 1) / n * 100)
    print(f"\rSaving GIF {out_path} … {f"{i + 1}/{n} ({pct}%)" if i + 1 != n else "Done !"}",
          end="\n" if (i + 1) == n else "")
# Save GIF
try:
    anim.save(out_path, writer='pillow', fps=fps, progress_callback=_progress)
    saved = True
except Exception as e:
    saved = False
    err = str(e)

plt.close(fig)  # prevent double display in some environments

# Show a confirmation + first frame snapshot to preview
# (Create and display a static preview frame)
fig_preview = plt.figure(figsize=(7.5, 6.5))
axp = fig_preview.add_subplot(111, projection='3d')
axp.view_init(elev=elev, azim=azim)
axp.plot_surface(X, Y, Z, rstride=2, cstride=2, linewidth=0, antialiased=True, alpha=0.9)
axp.plot([xy[0,0]], [xy[0,1]], [Z_traj[0]], marker='o', markersize=8, linestyle='')
axp.set_xlim(*xlim); axp.set_ylim(*ylim)
Zmin, Zmax = np.min(Z), np.max(Z); pad = 0.05*(Zmax - Zmin + 1e-12)
axp.set_zlim(Zmin - pad, Zmax + pad)
axp.set_xlabel("x"); axp.set_ylabel("y"); axp.set_zlabel("distorted V(x, y)")
axp.set_title("Preview: frame 0")
plt.show()

print("Saved GIF at:", out_path if saved else "Failed to save GIF")
if not saved:
    print("Error while saving GIF:", err)
