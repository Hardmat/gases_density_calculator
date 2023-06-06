import streamlit as st
import plotly.graph_objects as go
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
def calculate_density(gas_mixture, pressure, temperature):
    total_density = 0
    for gas, percentage in gas_mixture.items():
        molar_mass = gas_molar_masses[gas]
        molar_mass_kg = molar_mass / 1000  # kg/mol
        temperature_kelvin = temperature + 273.15  # Convert temperature to Kelvin
        pressure_atm = pressure / 14.6959488  # Convert pressure from PSI to atm
        density = (pressure_atm * molar_mass_kg) / (ideal_gas_constant * temperature_kelvin)
        density = density * molar_volume_conversion  # Convert from g/L to kg/m^3
        total_density += density * (percentage / 100)
    return total_density

# Streamlit app
st.title("Gaseous Density Calculator")

gas_mixture = {}
gas = st.selectbox("Select Gas", list(gas_molar_masses.keys()))
percentage = st.number_input("Percentage (%)", min_value=0, max_value=100, step=1)
gas_mixture[gas] = percentage

add_more_gases = st.checkbox("Add more gases")
while add_more_gases:
    gas = st.selectbox("Select Gas", list(gas_molar_masses.keys()))
    percentage = st.number_input("Percentage (%)", min_value=0, max_value=100, step=1)
    gas_mixture[gas] = percentage
    add_more_gases = st.checkbox("Add more gases")

pressure = st.slider("Pressure (PSI)", 0, 200, step=1)
temperature = st.slider("Temperature (°C)", 0, 80, step=1)

density = calculate_density(gas_mixture, pressure, temperature)
st.write("Density of the gas mixture:", density, "kg/m^3")

# Generate pressure and temperature values for the 3D plot
pressure_values = np.linspace(0, 200, 100)
temperature_values = np.linspace(0, 80, 100)

# Calculate density for each pressure and temperature combination
density_values = np.zeros((100, 100))
for i, pressure_val in enumerate(pressure_values):
    for j, temperature_val in enumerate(temperature_values):
        density_values[i, j] = calculate_density(gas_mixture, pressure_val, temperature_val)

# Create a meshgrid for the pressure and temperature values
pressure_grid, temperature_grid = np.meshgrid(pressure_values, temperature_values)

# Create a 3D plot of density using Plotly
fig = go.Figure(data=[go.Surface(z=density_values, x=pressure_grid, y=temperature_grid)])
fig.update_layout(
    scene=dict(
        xaxis_title="Pressure (PSI)",
        yaxis_title="Temperature (°C)",
        zaxis_title="Density (kg/m^3)",
        camera=dict(
            eye=dict(x=1.7, y=-1.7, z=0.5)
        )
    )
)

# Add a marker for the calculated density position
fig.add_trace(go.Scatter3d(
    x=[pressure],
    y=[temperature],
    z=[density],
    mode="markers",
    marker=dict(
        size=5,
        color="red"
    )
))

# Set the opacity of the plot
fig.update_traces(opacity=0.8)

# Display the plot using st.plotly_chart
st.plotly_chart(fig)
