# rectangular-channel-fill-
Lucas-Washburn simulator
Capillary Filling in a Rectangular Microchannel
A 1‑D Lucas–Washburn Simulator with Streamlit
This repository contains an interactive simulator for capillary‑driven filling in a rectangular microfluidic channel. The model is based on the Lucas–Washburn equation, adapted for rectangular geometries, and assumes 1‑D plug flow behind the advancing liquid front.
The app is built in Python and deployed using Streamlit, making it ideal for teaching, outreach, and rapid exploration of microfluidic design parameters.

🚀 Features
Geometry Controls
• 	Channel width
• 	Channel height
• 	Channel length
Fluid Properties
• 	Surface tension
• 	Viscosity
• 	Contact angle
Outputs
• 	Animated filling front along the channel
• 	Front position vs time
• 	Front velocity vs time
• 	Concentration profile (filled = 1, empty = 0)
• 	Estimated time to fill the channel

🧠 Model Overview
The simulator uses the Lucas–Washburn relation for capillary filling:

where the coefficient  depends on:
• 	surface tension
• 	contact angle
• 	viscosity
• 	channel width and height
• 	rectangular‑channel hydraulic resistance correction
The model assumes:
• 	No external pressure (pure capillary filling)
• 	Newtonian fluid
• 	1‑D plug flow behind the front
• 	No evaporation or dynamic contact angle effects
This keeps the physics transparent and ideal for teaching.
