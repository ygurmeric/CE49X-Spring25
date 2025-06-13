import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Union

class DataInput:
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.json']
        self.required_columns = [
            'product_id', 'product_name', 'life_cycle_stage', 'material_type',
            'quantity_kg', 'energy_consumption_kwh', 'transport_distance_km',
            'transport_mode', 'waste_generated_kg', 'recycling_rate',
            'landfill_rate', 'incineration_rate', 'carbon_footprint_kg_co2e',
            'water_usage_liters'
        ]

    def read_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Read data from various file formats.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

        if file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix == '.xlsx':
            return pd.read_excel(file_path)
        elif file_path.suffix == '.json':
            return pd.read_json(file_path)

    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate input data structure and content.
        """
        # Check all required columns exist
        for col in self.required_columns:
            if col not in data.columns:
                print(f"❌ Missing column: {col}")
                return False

        # Check numeric types
        numeric_columns = [
            'quantity_kg', 'energy_consumption_kwh', 'transport_distance_km',
            'waste_generated_kg', 'recycling_rate', 'landfill_rate',
            'incineration_rate', 'carbon_footprint_kg_co2e', 'water_usage_liters'
        ]
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(data[col]):
                print(f"❌ Column '{col}' must be numeric.")
                return False

        # Check that rates add up to approximately 1.0
        for i, row in data.iterrows():
            total = row['recycling_rate'] + row['landfill_rate'] + row['incineration_rate']
            if not (0.99 <= total <= 1.01):
                print(f"❌ Row {i}: recycling+landfill+incineration = {total} (must ≈ 1)")
                return False

        return True

    def read_impact_factors(self, file_path: Union[str, Path]) -> Dict:
        """
        Read impact factors from JSON file.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Impact factors file not found: {file_path}")

        if file_path.suffix != '.json':
            raise ValueError("Impact factors must be provided in JSON format")

        with open(file_path, 'r') as f:
            impact_factors = json.load(f)

        return impact_factors