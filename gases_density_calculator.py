import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Constants
gas_molar_masses = {
    "Oxygen": 32,  # g/mol
    "Nitrogen": 28.0134,
    "Hydrogen": 2.01588,
    "Helium": 4.002602,
    "Carbon Dioxide": 44.0095,
    "Argon": 39.948,
    "Methane": 16.04246,
    "Ethane": 30.06904,
    "Propane": 44.09562,
    "Butane": 58.12218
}

ideal_gas_constant = 0.0821  # atm * L / (mol * K)
molar_volume_conversion = 1000  # L/m^3

# Function to calculate density
def calculate_density(gas, pressure, temperature):
    molar_mass = gas_molar_masses[gas]
    molar_mass_kg = molar_mass / 1000  # kg/mol
    temperature_kelvin = temperature + 273.15  # Convert temperature to Kelvin
    pressure_atm = pressure / 14.6959488  # Convert pressure from PSI to atm
    density = (pressure_atm * molar_mass_kg) / (ideal_gas_constant * temperature_kelvin)
    density = density * molar_volume_conversion  # Convert from g/L to kg/m^3
    return density

# Streamlit app
st.title("Gaseous Density Calculator")

gas = st.selectbox("Select Gas", list(gas_molar_masses.keys()))
pressure = st.slider("Pressure (PSI)", 0, 200, step=1)
temperature = st.slider("Temperature (°C)", 0, 80, step=1)

density = calculate_density(gas, pressure, temperature)
st.write("Density of", gas, ":", density, "kg/m^3")

# Generate pressure and temperature values for the 3D plot
pressure_values = np.linspace(0, 200, 100)
temperature_values = np.linspace(0, 80, 100)

# Calculate density for each pressure and temperature combination
density_values = np.zeros((100, 100))
for i, pressure_val in enumerate(pressure_values):
    for j, temperature_val in enumerate(temperature_values):
        density_values[i, j] = calculate_density(gas, pressure_val, temperature_val)

# Create a meshgrid for the pressure and temperature values
pressure_grid, temperature_grid = np.meshgrid(pressure_values, temperature_values)

# Create a 3D plot of density
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(pressure_grid, temperature_grid, density_values, cmap="viridis")
ax.set_xlabel("Pressure (PSI)")
ax.set_ylabel("Temperature (°C)")
ax.set_zlabel("Density (kg/m^3)")

# Set the title of the graph based on the selected gas
ax.set_title(f"Density of {gas}")

# Add a red dot for the calculated density position
ax.scatter(pressure, temperature, density, color="red", s=50)

# Adjust the z-axis scale for better visualization
max_density = np.max(density_values)
ax.set_zlim(0, max_density + max_density * 0.1)

# Display the plot using st.pyplot
st.pyplot(fig)
