# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 17:37:04 2025

@author: martp
"""

# LW MODEL v3.0 — includes K_scale and temperature-dependent viscosity & surface tension

import numpy as np

def water_viscosity_mPa_s(T_C):
    """
    Temperature-dependent viscosity of water in mPa·s.
    Valid for 0–100 °C. Smooth empirical fit.
    """
    return 1.002 * np.exp(-0.032*(T_C - 20))  # good approximation


def water_surface_tension_Nm(T_C):
    """
    Temperature-dependent surface tension of water in N/m.
    Linear empirical fit around room temperature.
    """
    return 0.072 - 0.00015*(T_C - 20)


def capillary_fill_lucas_washburn(
    w=7.5e-4,
    h=1.25e-4,
    L_tot=1e-2,
    gamma=0.072,
    theta_deg=0.0,
    mu=1e-3,
    t_end=5.0,
    Nt=500,
    Nx=400,
    K_scale=1.0,
    T_C=20.0   # NEW: temperature in °C
):
    """
    Lucas–Washburn capillary filling in a rectangular microchannel.
    Includes:
    - K_scale calibration factor
    - Temperature-dependent viscosity and surface tension
    """

    # Override gamma and mu with temperature-dependent values
    mu = water_viscosity_mPa_s(T_C) * 1e-3      # convert mPa·s → Pa·s
    gamma = water_surface_tension_Nm(T_C)

    theta = np.deg2rad(theta_deg)

    rect_corr = 1.0 - 0.63 * (h / w)

    Pcap = gamma * np.cos(theta) * (1.0/h + 1.0/w)

    K = (Pcap * h**3 * w * rect_corr) / (12.0 * mu)
    K *= K_scale

    t = np.linspace(0.0, t_end, Nt)

    L = np.sqrt(2.0 * K * t)
    L = np.clip(L, 0.0, L_tot)

    v = np.gradient(L, t, edge_order=2)

    x = np.linspace(0.0, L_tot, Nx)

    C = np.zeros((Nt, Nx))
    for i in range(Nt):
        C[i, x <= L[i]] = 1.0

    t_fill = None
    if K > 0:
        t_fill_est = L_tot**2 / (2.0 * K)
        if t_fill_est <= t_end:
            t_fill = t_fill_est

    return t, x, L, v, C, t_fill, mu, gamma