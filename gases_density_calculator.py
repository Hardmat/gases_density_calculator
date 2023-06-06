import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import plotly.graph_objects as go

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
lbs_to_kg_conversion = 0.453592  # lbs to kg
gallon_to_liter_conversion = 3.78541  # gallon to liter
cubic_foot_to_liter_conversion = 28.3168  # cubic foot to liter

# Function to calculate density
def calculate_density(gas_mixture, pressure, temperature):
    total_percentage = sum(gas_mixture.values())
    if total_percentage != 100:
        st.error("Gas mixture percentages must add up to 100%.")
        return None
    density = 0
    for gas, percentage in gas_mixture.items():
        molar_mass = gas_molar_masses[gas]
        molar_mass_kg = molar_mass / 1000  # kg/mol
        mole_fraction = percentage / total_percentage
        temperature_kelvin = temperature + 273.15  # Convert temperature to Kelvin
        pressure_atm = pressure / 14.6959488  # Convert pressure from PSI to atm
        partial_density = (pressure_atm * molar_mass_kg) / (ideal_gas_constant * temperature_kelvin)
        density += partial_density * mole_fraction
    density = density * molar_volume_conversion  # Convert from g/L to kg/m^3
    return density

# Streamlit app
st.title("Gaseous Density Calculator")
st.markdown("This calculator is based on the ideal gas law and is a work in progress. Use it at your own discretion.")

gas_mixture = {}
selected_gases = st.multiselect("Select Gases", list(gas_molar_masses.keys()))
for gas in selected_gases:
    percentage = st.number_input(f"Percentage of {gas}", min_value=0, max_value=100, key=gas)
    gas_mixture[gas] = percentage

pressure = st.slider("Pressure (PSI)", 0, 200, step=1)
temperature = st.slider("Temperature (°C)", 0, 80, step=1)

density = calculate_density(gas_mixture, pressure, temperature)

if density is not None:
    st.write("Density of Gas Mixture:")
    st.write(f"- Kilograms per cubic meter: {density:.2f} kg/m^3")
    st.write(f"- Grams per liter: {density*1000:.2f} g/L")
    st.write(f"- Kilograms per liter: {density:.2f} kg/L")
    st.write(f"- Pounds per cubic foot: {density * lbs_to_kg_conversion / cubic_foot_to_liter_conversion:.2f} lb/ft^3")
    st.write(f"- Pounds per gallon: {density * lbs_to_kg_conversion / gallon_to_liter_conversion:.2f} lb/gal")

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
