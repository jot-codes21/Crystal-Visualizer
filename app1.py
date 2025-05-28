import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# -------------------- Core Logic Functions -------------------- #

def plot_structure(coordinates, edges, title, highlight_points=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])

    for edge in edges:
        poly = Poly3DCollection([edge], alpha=0.25, linewidths=1, edgecolors='r')
        poly.set_facecolor((0, 0, 1, 0.1))
        ax.add_collection3d(poly)

    x, y, z = zip(*coordinates)
    ax.scatter(x, y, z, color='b', s=50, label="Corner atoms")

    if highlight_points:
        hx, hy, hz = zip(*highlight_points)
        ax.scatter(hx, hy, hz, color='g', s=100, label="Face-centered atoms")

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 1.5)
    ax.set_zlim(0, 1.5)
    plt.title(title)
    plt.legend()
    st.pyplot(fig)

def display_bcc():
    coordinates = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)
    ]

    edges = [
        [coordinates[0], coordinates[1], coordinates[4], coordinates[2]],
        [coordinates[0], coordinates[1], coordinates[5], coordinates[3]],
        [coordinates[0], coordinates[2], coordinates[6], coordinates[3]],
        [coordinates[7], coordinates[6], coordinates[2], coordinates[4]],
        [coordinates[7], coordinates[6], coordinates[3], coordinates[5]],
        [coordinates[7], coordinates[4], coordinates[1], coordinates[5]],
    ]

    plot_structure(coordinates, edges, "BCC Crystal System")

def display_fcc():
    corner_coordinates = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)
    ]

    face_center_coordinates = [
        (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5),
        (0.5, 0.5, 1), (0.5, 1, 0.5), (1, 0.5, 0.5)
    ]

    edges = [
        [corner_coordinates[0], corner_coordinates[1], corner_coordinates[4], corner_coordinates[2]],
        [corner_coordinates[0], corner_coordinates[1], corner_coordinates[5], corner_coordinates[3]],
        [corner_coordinates[0], corner_coordinates[2], corner_coordinates[6], corner_coordinates[3]],
        [corner_coordinates[7], corner_coordinates[6], corner_coordinates[2], corner_coordinates[4]],
        [corner_coordinates[7], corner_coordinates[6], corner_coordinates[3], corner_coordinates[5]],
        [corner_coordinates[7], corner_coordinates[4], corner_coordinates[1], corner_coordinates[5]],
    ]

    plot_structure(corner_coordinates + face_center_coordinates, edges, "FCC Crystal System", face_center_coordinates)

def plot_plane(points, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])
    ax.add_collection3d(Poly3DCollection([points], alpha=0.5, facecolors='cyan'))
    x, y, z = zip(*points)
    ax.scatter(x, y, z, color='r', s=50)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.title(title)
    st.pyplot(fig)

def display_slip_plane_bcc(slip_plane):
    planes = {
        "(110)": [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)],
        "(112)": [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0.5, 0.5, 1)],
        "(123)": [(0, 0, 0), (1, 0, 0), (0.5, 1, 0.5), (0.33, 0.67, 1)],
    }
    if slip_plane in planes:
        plot_plane(planes[slip_plane], f"BCC Slip Plane {slip_plane}")
    else:
        st.error("Invalid BCC slip plane.")

def display_slip_plane_fcc(slip_plane):
    planes = {
        "(111)": [(0, 0, 1), (0, 1, 0), (1, 0, 0)],
        "(-111)": [(0, 0, -1), (0, -1, 0), (-1, 0, 0)],
        "(1-11)": [(1, 0, 0), (0, -1, 0), (0, 0, 1)],
        "(-1-11)": [(-1, 0, 0), (0, -1, 0), (0, 0, 1)],
    }
    if slip_plane in planes:
        plot_plane(planes[slip_plane], f"FCC Slip Plane {slip_plane}")
    else:
        st.error("Invalid FCC slip plane.")

# -------------------- Streamlit Interface -------------------- #

st.title("Crystal Plasticity Visualizer 🧊")

system = st.selectbox("Choose the Crystal System", ["BCC", "FCC"])

if system == "BCC":
    st.subheader("BCC Structure")
    display_bcc()
    slip_plane = st.selectbox("Select BCC Slip Plane", ["(110)", "(112)", "(123)"])
    display_slip_plane_bcc(slip_plane)

elif system == "FCC":
    st.subheader("FCC Structure")
    display_fcc()
    slip_plane = st.selectbox("Select FCC Slip Plane", ["(111)", "(-111)", "(1-11)", "(-1-11)"])
    display_slip_plane_fcc(slip_plane)
