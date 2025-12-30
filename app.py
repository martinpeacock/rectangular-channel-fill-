# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 17:37:38 2025

@author: martp
"""

import streamlit as st
import plotly.express as px

from lw_model import capillary_fill_lucas_washburn

st.set_page_config(
    page_title="Capillary Filling: Lucas–Washburn",
    layout="wide"
)

st.title("Capillary Filling in a Rectangular Microchannel")
st.markdown(
    "This app simulates **1‑D Lucas–Washburn capillary filling** in a rectangular microchannel. "
    "Now includes **temperature‑dependent viscosity and surface tension**."
)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("Geometry")
w_um = st.sidebar.number_input("Width [µm]", value=750.0, min_value=10.0, step=10.0)
h_um = st.sidebar.number_input("Height [µm]", value=125.0, min_value=5.0, step=5.0)
L_mm = st.sidebar.number_input("Length [mm]", value=10.0, min_value=1.0, step=1.0)

st.sidebar.header("Fluid Properties")
theta_deg = st.sidebar.slider("Contact angle [°]", min_value=0.0, max_value=120.0, value=0.0, step=1.0)

# NEW: Temperature slider
T_C = st.sidebar.slider("Temperature [°C]", min_value=5.0, max_value=60.0, value=20.0, step=1.0)

st.sidebar.header("Simulation Control")
t_end = st.sidebar.number_input("Simulation time [s]", value=5.0, min_value=0.1, step=0.5, format="%.2f")
Nt = st.sidebar.slider("Number of time points", min_value=100, max_value=1000, value=500, step=100)
Nx = st.sidebar.slider("Number of spatial points", min_value=100, max_value=800, value=400, step=100)

st.sidebar.header("Device Calibration")
K_scale = st.sidebar.number_input(
    "LW scaling factor (1 = ideal, ~6000 = device-like)",
    value=1.0,
    min_value=1.0,
    step=100.0
)

run = st.sidebar.button("Run simulation")

# Unit conversions
w = w_um * 1e-6
h = h_um * 1e-6
L_tot = L_mm * 1e-3

# ---------------------------------------------------------
# Run Simulation
# ---------------------------------------------------------
if run:
    with st.spinner("Running Lucas–Washburn simulation..."):
        t, x, L, v, C, t_fill, mu, gamma = capillary_fill_lucas_washburn(
            w=w,
            h=h,
            L_tot=L_tot,
            theta_deg=theta_deg,
            t_end=t_end,
            Nt=Nt,
            Nx=Nx,
            K_scale=K_scale,
            T_C=T_C
        )

    st.success(f"Temperature: {T_C} °C — viscosity = {mu*1e3:.3f} mPa·s, surface tension = {gamma:.4f} N/m")

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

    st.subheader("Filling Front and Concentration Profile")

    t_idx = st.slider(
        "Select time index",
        min_value=0,
        max_value=len(t) - 1,
        value=len(t) - 1
    )

    t_current = t[t_idx]
    L_current = L[t_idx]

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
    fig_c.update_xaxes(tickformat=".2f")
    st.plotly_chart(fig_c, use_container_width=True)

else:
    st.info("Adjust parameters in the sidebar and click **Run simulation** to begin.")