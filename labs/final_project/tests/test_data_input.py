"""
Tests for the data input module.
"""

import pytest
import pandas as pd
import json
from pathlib import Path
from src.data_input import DataInput

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'product_id': ['P001', 'P002', 'P003'],
        'product_name': ['A', 'B', 'C'],
        'life_cycle_stage': ['manufacturing']*3,
        'material_type': ['steel']*3,
        'quantity_kg': [100, 200, 300],
        'energy_consumption_kwh': [50, 100, 150],
        'transport_distance_km': [10, 20, 30],
        'transport_mode': ['truck']*3,
        'waste_generated_kg': [5, 10, 15],
        'recycling_rate': [0.8, 0.7, 0.6],
        'landfill_rate': [0.1, 0.2, 0.3],
        'incineration_rate': [0.1, 0.1, 0.1],  # Her satırda toplam = 1
        'carbon_footprint_kg_co2e': [20, 30, 40],
        'water_usage_liters': [100, 200, 300]
    })

@pytest.fixture
def sample_impact_factors():
    """Create sample impact factors for testing."""
    return {
        'steel': {
            'manufacturing': {
                'carbon_impact': 1.8,
                'energy_impact': 20,
                'water_impact': 150
            },
            'transportation': {
                'carbon_impact': 0.5,
                'energy_impact': 5,
                'water_impact': 30
            },
            'end-of-life': {
                'carbon_impact': 0.1,
                'energy_impact': 1,
                'water_impact': 10
            }
        }
    }

def test_read_data_csv(sample_data, tmp_path):
    """Test reading CSV data."""
    data_input = DataInput()
    
    # Save sample data to temporary CSV file
    csv_file = tmp_path / "test_data.csv"
    sample_data.to_csv(csv_file, index=False)
    
    # Read the data back
    data = data_input.read_data(csv_file)
    
    assert isinstance(data, pd.DataFrame)
    assert len(data) == len(sample_data)
    assert all(col in data.columns for col in sample_data.columns)

def test_read_data_json(sample_impact_factors, tmp_path):
    """Test reading JSON data."""
    data_input = DataInput()
    
    # Save sample impact factors to temporary JSON file
    json_file = tmp_path / "test_impact_factors.json"
    with open(json_file, 'w') as f:
        json.dump(sample_impact_factors, f)
    
    # Read the data back
    data = data_input.read_data(json_file)
    
    assert isinstance(data, pd.DataFrame)
    assert not data.empty

def test_validate_data(sample_data):
    data_input = DataInput()
    assert data_input.validate_data(sample_data)

    """Test data validation."""
    data_input = DataInput()
    
    # Test valid data
    assert data_input.validate_data(sample_data)
    
    # Test missing required column
    invalid_data = sample_data.drop('product_id', axis=1)
    assert not data_input.validate_data(invalid_data)
    
    # Test invalid numeric data
    invalid_data = sample_data.copy()
    invalid_data.loc[0, 'quantity_kg'] = 'invalid'
    assert not data_input.validate_data(invalid_data)
    
    # Test invalid rates
    invalid_data = sample_data.copy()
    invalid_data.loc[0, 'recycling_rate'] = 0.6
    invalid_data.loc[0, 'landfill_rate'] = 0.6
    invalid_data.loc[0, 'incineration_rate'] = 0.6
    assert not data_input.validate_data(invalid_data)

def test_read_impact_factors(sample_impact_factors, tmp_path):
    """Test reading impact factors."""
    data_input = DataInput()
    
    # Save sample impact factors to temporary JSON file
    json_file = tmp_path / "test_impact_factors.json"
    with open(json_file, 'w') as f:
        json.dump(sample_impact_factors, f)
    
    # Read the impact factors
    factors = data_input.read_impact_factors(json_file)
    
    assert isinstance(factors, dict)
    assert 'steel' in factors
    assert 'manufacturing' in factors['steel']
    assert 'carbon_impact' in factors['steel']['manufacturing'] 