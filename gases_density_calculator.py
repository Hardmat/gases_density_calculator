# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:49:17 2023

@author: GUILLAUME.PAUL
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Constants
gas_molar_masses = {
    "Nitrogen": 28.0134,  # g/mol
    "Oxygen": 31.9988,  # g/mol
    "Hydrogen": 2.01588,  # g/mol
    "Carbon Dioxide": 44.0095,  # g/mol
    "Argon": 39.948,  # g/mol
    "Acetylene": 26.0373,  # g/mol
    "Ammonia": 17.0306,  # g/mol
    "Chlorine": 70.906,  # g/mol
    "Sulfur Dioxide": 64.0638,  # g/mol
    "Methane": 16.0425  # g/mol
}

ideal_gas_constant = 0.0821  # atm * L / (mol * K)
molar_volume_conversion = 1000  # L/m^3

# Function to calculate density
def calculate_density(pressure, temperature, gas):
    molar_mass = gas_molar_masses[gas]  # Get the molar mass of the selected gas
    temperature_kelvin = temperature + 273.15  # Convert temperature to Kelvin
    pressure_atm = pressure / 14.6959488  # Convert pressure from PSI to atm
    density = (pressure_atm * molar_mass) / (ideal_gas_constant * temperature_kelvin)
    density = density * molar_volume_conversion  # Convert from g/L to kg/m^3
    return density

# Streamlit app
st.title("Gas Density Calculator")

# Gas selection
selected_gas = st.selectbox("Select Gas", list(gas_molar_masses.keys()))

pressure = st.slider("Pressure (PSI)", 0, 200, step=1)
temperature = st.slider("Temperature (°C)", 0, 80, step=1)

density = calculate_density(pressure, temperature, selected_gas)
st.write(f"Density of {selected_gas}: {density} kg/m^3")

# Generate pressure and temperature values
pressure_values = np.linspace(0, 200, 100)
temperature_values = np.linspace(0, 80, 100)

# Calculate density for each pressure and temperature combination
density_values = np.zeros((100, 100))
for i, pressure_val in enumerate(pressure_values):
    for j, temperature_val in enumerate(temperature_values):
        density_values[i, j] = calculate_density(pressure_val, temperature_val, selected_gas)

# Create a meshgrid for the pressure and temperature values
pressure_grid, temperature_grid = np.meshgrid(pressure_values, temperature_values)

# Create a 3D plot of density
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(pressure_grid, temperature_grid, density_values, cmap="viridis")
ax.set_xlabel("Pressure (PSI)")
ax.set_ylabel("Temperature (°C)")
ax.set_zlabel("Density (kg/m^3)")
ax.set_title(f"{selected_gas} Density")

# Add a red dot for the calculated density position
ax.scatter(pressure, temperature, density, color="red", s=50)

# Display the plot using st.pyplot
st.pyplot(fig)