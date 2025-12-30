# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 09:29:22 2025

@author: martp
"""

# LW MODEL v2.0 — includes K_scale calibration factor

import numpy as np

def capillary_fill_lucas_washburn(
    w=7.5e-4,      # width [m]
    h=1.25e-4,     # height [m]
    L_tot=1e-2,    # total channel length [m]
    gamma=0.072,   # surface tension [N/m]
    theta_deg=0.0, # contact angle [degrees]
    mu=1e-3,       # viscosity [Pa·s]
    t_end=5.0,     # simulation time [s]
    Nt=500,        # number of time points
    Nx=400,        # number of spatial points
    K_scale=1.0    # calibration factor (1 = ideal LW)
):
    """
    Lucas–Washburn capillary filling in a rectangular microchannel.
    Includes a scaling factor K_scale to match real device behaviour.
    """

    # Convert contact angle to radians
    theta = np.deg2rad(theta_deg)

    # Geometric correction factor for rectangular cross-section
    rect_corr = 1.0 - 0.63 * (h / w)

    # Capillary pressure (approximation for rectangular channels)
    Pcap = gamma * np.cos(theta) * (1.0/h + 1.0/w)

    # Lucas–Washburn coefficient K
    K = (Pcap * h**3 * w * rect_corr) / (12.0 * mu)

    # Apply calibration factor
    K *= K_scale

    # Time grid
    t = np.linspace(0.0, t_end, Nt)

    # Front position
    L = np.sqrt(2.0 * K * t)
    L = np.clip(L, 0.0, L_tot)

    # Front velocity (numerical derivative)
    v = np.gradient(L, t, edge_order=2)

    # Spatial grid
    x = np.linspace(0.0, L_tot, Nx)

    # Concentration field: 1 behind the front, 0 ahead
    C = np.zeros((Nt, Nx))
    for i in range(Nt):
        C[i, x <= L[i]] = 1.0

    # Time to fill channel: solve L(t_fill) = L_tot
    t_fill = None
    if K > 0:
        t_fill_est = L_tot**2 / (2.0 * K)
        if t_fill_est <= t_end:
            t_fill = t_fill_est

    return t, x, L, v, C, t_fill