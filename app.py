import streamlit as st
import plotly.express as px

from lw_model import capillary_fill_lucas_washburn

# ---------------------------------------------------------
# Streamlit Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Capillary Filling: Lucas–Washburn",
    layout="wide"
)

st.title("Capillary Filling in a Rectangular Microchannel")
st.markdown(
    "This app simulates **1‑D Lucas–Washburn capillary filling** in a rectangular microchannel. "
    "The filled region is represented as concentration = 1, and the unfilled region as 0."
)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("Geometry")
w_um = st.sidebar.number_input("Width [µm]", value=750.0, min_value=10.0, step=10.0)
h_um = st.sidebar.number_input("Height [µm]", value=125.0, min_value=5.0, step=5.0)
L_mm = st.sidebar.number_input("Length [mm]", value=10.0, min_value=1.0, step=1.0)

st.sidebar.header("Fluid Properties")
gamma = st.sidebar.number_input("Surface tension [N/m]", value=0.072, format="%.3f")
mu_mPa_s = st.sidebar.number_input("Viscosity [mPa·s]", value=1.0, min_value=0.1, step=0.1, format="%.2f")
theta_deg = st.sidebar.slider("Contact angle [°]", min_value=0.0, max_value=120.0, value=0.0, step=1.0)

st.sidebar.header("Simulation Control")
t_end = st.sidebar.number_input("Simulation time [s]", value=5.0, min_value=0.1, step=0.5, format="%.2f")
Nt = st.sidebar.slider("Number of time points", min_value=100, max_value=1000, value=500, step=100)
Nx = st.sidebar.slider("Number of spatial points", min_value=100, max_value=800, value=400, step=100)

run = st.sidebar.button("Run simulation")

# Unit conversions
w = w_um * 1e-6
h = h_um * 1e-6
L_tot = L_mm * 1e-3
mu = mu_mPa_s * 1e-3  # mPa·s → Pa·s

# ---------------------------------------------------------
# Run Simulation
# ---------------------------------------------------------
if run:
    with st.spinner("Running Lucas–Washburn simulation..."):
        t, x, L, v, C, t_fill = capillary_fill_lucas_washburn(
            w=w,
            h=h,
            L_tot=L_tot,
            gamma=gamma,
            theta_deg=theta_deg,
            mu=mu,
            t_end=t_end,
            Nt=Nt,
            Nx=Nx
        )

    # -----------------------------------------------------
    # Front Position and Velocity Plots
    # -----------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Front Position vs Time")
        fig_L = px.line(
            x=t, y=L,
            labels={"x": "Time [s]", "y": "Front Position [m]"},
            title="Lucas–Washburn Front Position"
        )
        st.plotly_chart(fig_L, use_container_width=True)

        if t_fill is not None:
            st.info(f"Estimated time to fill the channel: **{t_fill:.3f} s**")
        else:
            st.warning("Channel not fully filled within simulation time.")

    with col2:
        st.subheader("Front Velocity vs Time")
        fig_v = px.line(
            x=t, y=v,
            labels={"x": "Time [s]", "y": "Front Velocity [m/s]"},
            title="Front Velocity"
        )
        st.plotly_chart(fig_v, use_container_width=True)

    # -----------------------------------------------------
    # Concentration Profile (x-axis now in mm and formatted)
    # -----------------------------------------------------
    st.subheader("Filling Front and Concentration Profile")

    t_idx = st.slider(
        "Select time index",
        min_value=0,
        max_value=len(t) - 1,
        value=len(t) - 1
    )

    t_current = t[t_idx]
    L_current = L[t_idx]

    # Convert x-axis to mm
    x_mm = x * 1e3
    L_current_mm = L_current * 1e3

    st.markdown(
        f"**Time:** {t_current:.4f} s &nbsp;&nbsp; "
        f"**Front position:** {L_current_mm:.2f} mm"
    )

    fig_c = px.line(
        x=x_mm,
        y=C[t_idx, :],
        labels={"x": "Position [mm]", "y": "Concentration"},
        title="Concentration Profile (1 = filled, 0 = empty)"
    )
    fig_c.update_yaxes(range=[-0.1, 1.1])
    fig_c.update_xaxes(tickformat=".2f")  # ← ensures mm display
    st.plotly_chart(fig_c, use_container_width=True)

else:
    st.info("Adjust parameters in the sidebar and click **Run simulation** to begin.")