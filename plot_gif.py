# Create an animation showing a round robot moving +1 m, -2 m, +1 m along a curvilinear path,
# with the robot body drawn (circle + wheels) and an orientation arrow.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, transforms, animation

from file_opener import *


def create_animation(states, filename, show_robot=True, custom_pad_x=None, custom_pad_y=None, aspect_equal=True, mp4=False):
    # --- Set up figure/axes ---
    fig, ax = plt.subplots(figsize=(4,4))
    if aspect_equal:
        ax.set_aspect("equal", "box")
    ax.set_facecolor("#efefef")
    ax.grid(True, alpha=0.3)

    # Bounds
    xmin, ymin = states[:,0].min(), states[:,1].min()
    xmax, ymax = states[:,0].max(), states[:,1].max()
    d = max(xmax - xmin, ymax - ymin)
    d = max(d, 0.1)
    pad_x = 0.14 * d if custom_pad_x is None else custom_pad_x
    pad_y = 0.14 * d if custom_pad_y is None else custom_pad_y
    ax.set_xlim(xmin - pad_x, xmax + pad_x)
    ax.set_ylim(ymin - pad_y, ymax + pad_y)

    # Path line (trace of where the robot has been)
    trace_line, = ax.plot([], [], linewidth=2, alpha=0.5)
    if show_robot:
        # --- Robot drawing in its local frame (centered at origin, facing +x) ---
        R = 0.12 * d # robot radius [m]
        # Body
        body = patches.Circle((0, 0), R, facecolor="#dddddd", edgecolor="black", linewidth=2)
        # Wheels as two black rectangles in local frame, pre-rotated a bit to look like the example
        wheel_w, wheel_h = 0.06 * d, 0.02 * d  # [m]
        wheel1 = patches.Rectangle((-0.03 * d, 0.06 * d), wheel_w, wheel_h, facecolor="black", edgecolor="black")
        wheel2 = patches.Rectangle((-0.03 * d, -0.08 * d), wheel_w, wheel_h, facecolor="black", edgecolor="black")
        # Local decorative rotations to mimic the screenshot

        # Heading arrow (from center along +x in local frame)
        arrow_len = 0.1*d
        arrow = patches.FancyArrow(0, 0, arrow_len, 0, width=0.01*d, length_includes_head=True, edgecolor=None, facecolor="blue", alpha=0.8)

        # Add artists
        for art in (body, wheel1, wheel2, arrow):
            ax.add_patch(art)

        # Helper to update transforms for the robot at pose (x, y, theta)
        def set_robot_pose(x, y, theta):
            T = transforms.Affine2D().rotate(theta).translate(x, y) + ax.transData
            body.set_transform(T)
            wheel1.set_transform(T)
            wheel2.set_transform(T)
            arrow.set_transform(T)

        # Initialize
        set_robot_pose(states[0,0], states[0,1], states[0,2])

        # --- Animation update ---
        def update(i):
            # Update trace
            trace_line.set_data(states[:i+1, 0], states[:i+1, 1])
            # Update robot pose
            x, y, th = states[i]
            set_robot_pose(x, y, th)
            return trace_line, body, wheel1, wheel2, arrow
        # Create animation
        frames = len(states)
        ani = animation.FuncAnimation(fig, update, frames=range(0, frames, 4), interval=25, blit=True)
    else:
        frames = len(states)

        def update(i):
            trace_line.set_data(states[:i+1, 0], states[:i+1, 1])
            return trace_line,

        ani = animation.FuncAnimation(fig, update, frames=range(0, frames, 4), interval=25, blit=True)

    def _progress(i, n):
        pct = int((i + 1) / n * 100)
        print(f"\rSaving GIF {filename} … {f"{i + 1}/{n} ({pct}%)" if i+1 != n else "Done !"}", end="\n" if (i+1) == n else "")
    # Save as GIF
    try:
        writer = animation.FFMpegWriter(fps=40, codec="h264_nvenc", extra_args=["-preset", "p4"])
    except Exception:
        writer = animation.FFMpegWriter(fps=40, codec="libx264", extra_args=["-preset", "veryfast"])
    if mp4:
        gif_path = filename + ".mp4" if not filename.endswith(".mp4") else filename
        ani.save(gif_path, writer=writer, dpi=110, progress_callback=_progress)
    else:
        gif_path = filename + ".gif" if not filename.endswith(".gif") else filename
        ani.save(gif_path, writer="pillow", progress_callback=_progress)

def create_animation_carrot(states, carrot_states, filename, custom_pad_x=None, custom_pad_y=None, aspect_equal=True, mp4=False):
    # --- Set up figure/axes ---
    fig, ax = plt.subplots(figsize=(6,6))
    if aspect_equal:
        ax.set_aspect("equal", "box")
    ax.set_facecolor("#efefef")
    ax.grid(True, alpha=0.3)


    # Bounds
    xmin, ymin = states[:,0].min(), states[:,1].min()
    xmax, ymax = states[:,0].max(), states[:,1].max()
    d = max(xmax - xmin, ymax - ymin)
    d = max(d, 0.1)
    pad_x = 0.14 * d if custom_pad_x is None else custom_pad_x
    pad_y = 0.14 * d if custom_pad_y is None else custom_pad_y
    ax.set_xlim(xmin - pad_x, xmax + pad_x)
    ax.set_ylim(ymin - pad_y, ymax + pad_y)

    # Path line (trace of where the robot has been)
    trace_line, = ax.plot([], [], "r", linewidth=2, alpha=0.5)
    carrot_line, = ax.plot([], [], "g", linewidth=2, alpha=0.5)
    # --- Robot drawing in its local frame (centered at origin, facing +x) ---
    R = 0.12 * d # robot radius [m]
    # Body
    body = patches.Circle((0, 0), R, facecolor="#dddddd", edgecolor="black", linewidth=2)
    carrot = patches.Circle((0,0), R*0.4, facecolor="orange")

    # Wheels as two black rectangles in local frame, pre-rotated a bit to look like the example
    wheel_w, wheel_h = 0.06 * d, 0.02 * d  # [m]
    wheel1 = patches.Rectangle((-0.03 * d, 0.06 * d), wheel_w, wheel_h, facecolor="black", edgecolor="black")
    wheel2 = patches.Rectangle((-0.03 * d, -0.08 * d), wheel_w, wheel_h, facecolor="black", edgecolor="black")
    # Local decorative rotations to mimic the screenshot

    # Heading arrow (from center along +x in local frame)
    arrow_len = 0.1*d
    arrow = patches.FancyArrow(0, 0, arrow_len, 0, width=0.01*d, length_includes_head=True, edgecolor=None, facecolor="blue", alpha=0.8)

    # Add artists
    for art in (body, wheel1, wheel2, arrow, carrot):
        ax.add_patch(art)

    # Helper to update transforms for the robot at pose (x, y, theta)
    def set_robot_pose(x, y, theta, x_carrot, y_carrot):
        T = transforms.Affine2D().rotate(theta).translate(x, y) + ax.transData
        G = transforms.Affine2D().translate(x_carrot, y_carrot) + ax.transData
        body.set_transform(T)
        wheel1.set_transform(T)
        wheel2.set_transform(T)
        arrow.set_transform(T)
        carrot.set_transform(G)

    # Initialize
    set_robot_pose(states[0,0], states[0,1], states[0,2], carrot_states[0,0], carrot_states[0,1])

    # --- Animation update ---
    def update(i):
        # Update trace
        trace_line.set_data(states[:i+1, 0], states[:i+1, 1])
        carrot_line.set_data(carrot_states[:i+1, 0], carrot_states[:i+1, 1])
        # Update robot pose
        x, y, th = states[i]
        x_carrot, y_carrot = carrot_states[i]
        set_robot_pose(x, y, th, x_carrot, y_carrot)
        return trace_line, body, wheel1, wheel2, arrow, carrot, carrot_line
    # Create animation
    frames = len(states)
    ani = animation.FuncAnimation(fig, update, frames=range(0, frames, 4), interval=25, blit=True)
    def _progress(i, n):
        pct = int((i + 1) / n * 100)
        print(f"\rSaving GIF {filename} … {f"{i + 1}/{n} ({pct}%)" if i+1 != n else "Done !"}", end="\n" if (i+1) == n else "")
    try:
        writer = animation.FFMpegWriter(fps=40, codec="h264_nvenc", extra_args=["-preset", "p4"])
    except Exception:
        writer = animation.FFMpegWriter(fps=40, codec="libx264", extra_args=["-preset", "veryfast"])
    if mp4:
        gif_path = filename + ".mp4" if not filename.endswith(".mp4") else filename
        ani.save(gif_path, writer=writer, dpi=110, progress_callback=_progress)
    else:
        gif_path = filename + ".gif" if not filename.endswith(".gif") else filename
        ani.save(gif_path, writer="pillow", progress_callback=_progress)


bc_zn_angle = open_file("BenchmarkCurve1751138133.bin", False)

states = np.array([(r.x, r.y, r.a/180*np.pi) for r in bc_zn_angle])
carrot_states = np.array([(r.target_x, r.target_y) for r in bc_zn_angle])
carrot_states -= states[:, 0:2]
states[:, 0:2] = 0
create_animation_carrot(states, carrot_states, filename="ShowCurveEvolution")

states = np.array([(r.dt, r.rotational_target_deg, 0) for r in bc_zn_angle])
create_animation(states, filename="RampRotationalTarget", show_robot=False, custom_pad_x=0.5, custom_pad_y=100, aspect_equal=False, mp4=True)

states = np.array([(r.dt, r.rotational_position_deg, 0) for r in bc_zn_angle])
create_animation(states, filename="RampRotationalPosition", show_robot=False, custom_pad_x=0.5, custom_pad_y=100, aspect_equal=False, mp4=True)



"""
states = np.array([(r.dt, r.translational_target, 0) for r in bc_zn_angle])
create_animation(states, filename="RampDistanceInPosition", show_robot=False, custom_pad_x=0.5, custom_pad_y=100, aspect_equal=False)

states = np.array([(r.dt, r.translational_ramp_speed, 0) for r in bc_zn_angle])
create_animation(states, filename="RampDistanceInSpeed", show_robot=False, custom_pad_x=0.5, custom_pad_y=100, aspect_equal=False)
"""

