# Python Documentation for LCA Tool

## Overview

This Python-based Life Cycle Assessment (LCA) tool is designed to calculate and visualize environmental impacts associated with various products or processes over their entire life cycle. The tool integrates structured data management, impact factor handling, comprehensive validation, detailed calculations, and high-quality visual outputs. It supports multiple file formats and is modular, making it easy to maintain and expand.

---

## Project Structure

```
final_project/
│
├── main.py                     # Entry point for executing the analysis
├── data/
│   ├── raw/                    # Contains raw input CSV, JSON, or Excel data
│   └── processed/              # Stores processed output files (e.g. impact_results.csv)
├── src/
│   ├── data_input.py           # Handles reading and validation of input data
│   ├── calculations.py         # Performs environmental impact calculations
│   ├── visualization.py        # Generates plots and visual reports
│   ├── utils.py                # Utility functions (e.g., grouping, formatting)
├── tests/
│   ├── test_data_input.py      # Unit tests for data reading and validation
│   ├── test_calculations.py    # Unit tests for impact calculations
│   └── test_visualization.py   # Unit tests for graph generation
└── impact_factors.json         # Database of environmental impact factors
```

---

## Modules Description

### 1. `data_input.py`

**Purpose:** Handles loading of raw data and validation of the input format.

* `read_data(file_path)`

  * Supports `.csv`, `.xlsx`, and `.json`
  * Returns a validated pandas DataFrame

* `validate_data(data)`

  * Verifies presence of required columns
  * Confirms numeric values in impact-related columns
  * Ensures that waste rates sum up to 1

* `read_impact_factors(file_path)`

  * Loads a JSON file containing impact multipliers by material and stage

### 2. `calculations.py`

**Purpose:** Applies environmental formulas to calculate per-category impact values.

* `calculate_impacts(data)`

  * Multiplies quantity or energy values with impact factors
  * Adds columns: `carbon_impact`, `energy_impact`, `water_impact`

* `compare_alternatives(data, product_ids)`

  * Filters and compares impact data of selected product IDs

### 3. `visualization.py`

**Purpose:** Visualizes the results via charts and plots using matplotlib.

* `plot_carbon_by_material(data)`
* `plot_carbon_by_stage(data)`
* `plot_life_cycle_impacts(data, product_id)`
* `plot_product_comparison(data, product_ids)`
* `plot_end_of_life_breakdown(data, product_id)`
* `plot_impact_correlation(data)`

### 4. `utils.py`

**Purpose:** Helper functions for formatting and aggregation.

* `group_and_sum(data, group_cols, sum_cols)`
* `ensure_directory(path)`

---

## Execution Flow (`main.py`)

1. Load input product data from raw CSV
2. Validate input structure
3. Track life cycle stage distribution
4. Load impact factors
5. Calculate environmental impacts
6. Save results to processed directory
7. Generate six types of plots:

   * By material
   * By life cycle stage
   * Per-product life cycle
   * Product comparison (radar)
   * End-of-life breakdown
   * Category correlation

---

## Environmental Metrics Computed

* **Carbon Footprint (kg CO2e)**: Calculated using material-specific emission factors
* **Energy Consumption (kWh)**: Based on energy used in manufacturing and transport
* **Water Usage (liters)**: Water required in production and disposal
* **Waste Management**: Tracks recycling, landfill, and incineration percentages

---

## Supported File Formats

* `.csv`, `.xlsx`, `.json` for input
* `.png` for graphs
* `.csv` for output tables

---

## Unit Testing (with pytest)

Tests are organized under `tests/` and cover all core components.

### Sample Tests

* `test_validate_data()` ensures all validation rules are enforced
* `test_calculate_impacts()` checks numeric accuracy of environmental calculations
* `test_compare_alternatives()` verifies product-to-product impact comparisons
* `test_visualization()` confirms chart generation runs without exception

### Failures Resolved

* Test initially expected 2 comparison results; logic was updated to handle life cycle stages properly
* Validation test failed due to incorrect rate sum or type mismatch (e.g., string in numeric column); sample data updated accordingly

---

## Output Artifacts

* `impact_results.csv`: Tabular summary of calculated impacts
* Graphs:

  * `impact_breakdown_by_material.png`
  * `life_cycle_carbon_by_stage.png`
  * `life_cycle_impact_P001.png`
  * `product_comparison_radar.png`
  * `end_of_life_P001.png`
  * `impact_correlation.png`

---

## Notes

* Modular structure allows replacing impact factor sources or data sources without rewriting logic
* Input format must strictly follow schema for validation to succeed
* Tool designed to support future enhancements like normalization, weighting, and benchmarking against targets

---

## Conclusion

This tool provides a fully automated pipeline from raw data input to visual impact assessment, ensuring consistency, accuracy, and usability for environmental engineers, sustainability analysts, or academic researchers. Thanks to its test coverage and modularity, it can be deployed in diverse scenarios ranging from construction materials to consumer products.

---
