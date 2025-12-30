# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 07:23:43 2025

@author: martp
"""

import numpy as np

def capillary_fill_lucas_washburn(
    w=7.5e-4,      # width [m]
    h=1.25e-4,     # height [m]
    L_tot=1e-2,    # total channel length [m]
    gamma=0.072,   # surface tension [N/m]
    theta_deg=0.0, # contact angle [degrees]
    mu=1e-3,       # viscosity [Pa·s]
    t_end=5.0,     # simulation time [s]
    Nt=500,        # time points
    Nx=400         # spatial grid
):
    """
    Lucas–Washburn capillary filling in a rectangular microchannel.

    Returns:
        t: time array [s]
        x: spatial array [m]
        L: front position vs time [m]
        v: front velocity vs time [m/s]
        C: concentration field (1 behind front, 0 ahead), shape (Nt, Nx)
        t_fill: time to fill channel completely [s] (or None if not filled)
    """

    theta = np.deg2rad(theta_deg)

    # Geometric correction factor for rectangular cross-section
    rect_corr = 1.0 - 0.63 * (h / w)

    # Capillary pressure (approx for rectangular)
    Pcap = gamma * np.cos(theta) * (1.0/h + 1.0/w)

    # Lucas–Washburn coefficient K in L(t) = sqrt(2 K t)
    # Derived from balance of capillary pressure and viscous resistance
    K = (Pcap * h**3 * w * rect_corr) / (12.0 * mu)

    # Time grid
    t = np.linspace(0.0, t_end, Nt)

    # Front position
    L = np.sqrt(2.0 * K * t)
    L = np.clip(L, 0.0, L_tot)

    # Front velocity (numerical derivative)
    # add small epsilon to avoid issues at t=0 when differentiated
    v = np.gradient(L, t, edge_order=2)

    # Space grid
    x = np.linspace(0.0, L_tot, Nx)

    # Simple "concentration": 1 if filled, 0 if empty
    C = np.zeros((Nt, Nx))
    for i in range(Nt):
        C[i, x <= L[i]] = 1.0

    # Time to fill channel: solve L(t_fill) = L_tot => L_tot^2 = 2 K t_fill
    t_fill = None
    if K > 0.0:
        t_fill_est = L_tot**2 / (2.0 * K)
        if t_fill_est <= t_end:
            t_fill = t_fill_est

    return t, x, L, v, C, t_fill