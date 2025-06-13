
from src.visualization import LCAVisualizer
import pytest
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


@pytest.fixture(scope="session", autouse=True)
def patch_style():
    # Patch matplotlib style globally in tests
    plt.style.use('seaborn-v0_8')  # or 'default' if not available

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'product_id': ['P001'] * 3 + ['P002'] * 3,
        'product_name': ['Product1'] * 3 + ['Product2'] * 3,
        'life_cycle_stage': ['Manufacturing', 'Transportation', 'End-of-Life'] * 2,
        'material_type': ['steel'] * 3 + ['aluminum'] * 3,
        'quantity_kg': [100] * 6,
        'energy_consumption_kwh': [120, 20, 50, 180, 25, 20],
        'transport_distance_km': [50, 100, 30, 180, 140, 35],
        'transport_mode': ['Truck'] * 6,
        'waste_generated_kg': [5, 0, 100, 1, 0, 20],
        'recycling_rate': [0.9, 0, 0.9, 0.85, 0, 0.85],
        'landfill_rate': [0.05, 0, 0.05, 0.1, 0, 0.1],
        'incineration_rate': [0.05, 0, 0.05, 0.05, 0, 0.05],
        'carbon_footprint_kg_co2e': [180, 50, 10, 125, 30, 5],
        'water_usage_liters': [150, 30, 10, 100, 0, 6],
        'carbon_impact': [180, 50, 10, 125, 30, 5],
        'energy_impact': [120, 20, 50, 180, 25, 20],
        'water_impact': [150, 30, 10, 100, 0, 6]
    })

def test_plot_impact_breakdown(sample_data):
    vis = LCAVisualizer()
    fig = vis.plot_impact_breakdown(sample_data, 'carbon_impact', 'material_type')
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_life_cycle_impacts(sample_data):
    vis = LCAVisualizer()
    fig = vis.plot_life_cycle_impacts(sample_data, 'P001')
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_product_comparison(sample_data):
    vis = LCAVisualizer()
    fig = vis.plot_product_comparison(sample_data, ['P001', 'P002'])
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_end_of_life_breakdown(sample_data):
    vis = LCAVisualizer()
    fig = vis.plot_end_of_life_breakdown(sample_data, 'P001')
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_impact_correlation(sample_data):
    vis = LCAVisualizer()
    fig = vis.plot_impact_correlation(sample_data)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)