import os
import pandas as pd
from src.data_input import DataInput
from src.calculations import LCACalculator
from src.visualization import LCAVisualizer
from src.utils import save_results

def main():
    data_path = "data/raw/sample_data.csv"
    impact_factors_path = "data/raw/impact_factors.json"
    output_path = "data/processed/impact_results.csv"

    data_input = DataInput()

    # Step 1: Read product data
    try:
        print("Reading product data...")
        df = data_input.read_data(data_path)
        print("Product data loaded.")
    except Exception as e:
        print(f"Error reading product data: {e}")
        return

    # Step 2: Validate product data
    try:
        print("Validating product data...")
        data_input.validate_data(df)
        print("Product data is valid.")
    except Exception as e:
        print(f"Data validation failed: {e}")
        return

    # Step 3: Track life cycle stages
    try:
        print("\nLife cycle stage tracking:")
        stage_counts = df['life_cycle_stage'].str.lower().value_counts()
        for stage, count in stage_counts.items():
            print(f"  - {stage}: {count} entries")
    except Exception as e:
        print(f"Could not generate stage stats: {e}")

    # Step 4: Calculate environmental impacts
    try:
        print("\nCalculating environmental impacts...")
        calculator = LCACalculator(impact_factors_path)
        impacts_df = calculator.calculate_impacts(df)
        print("Environmental impacts calculated.")

        print("\nSample impact results:")
        print(impacts_df.head())
    except Exception as e:
        print(f"Impact calculation failed: {e}")
        return

    # Step 5: Save results to file
    try:
        print("\nSaving results...")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        save_results(impacts_df, output_path)
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"Failed to save results: {e}")

    # Step 6: Visualize results
    try:
        visualizer = LCAVisualizer()

        print("\nVisualizing carbon impact by material...")
        fig1 = visualizer.plot_impact_breakdown(impacts_df, 'carbon_impact', 'material_type')
        fig1.show()

        print("\nVisualizing carbon impact by life cycle stage...")
        fig2 = visualizer.plot_impact_breakdown(impacts_df, 'carbon_impact', 'life_cycle_stage')
        fig2.show()

        print("\nVisualizing total impacts by life cycle stage for product P001...")
        fig3 = visualizer.plot_life_cycle_impacts(impacts_df, product_id="P001")
        fig3.show()

        print("\nVisualizing product comparison (radar chart)...")
        product_ids = impacts_df['product_id'].unique().tolist()
        fig4 = visualizer.plot_product_comparison(impacts_df, product_ids=product_ids)
        fig4.show()

        print("\nVisualizing end-of-life management breakdown for product P001...")
        fig5 = visualizer.plot_end_of_life_breakdown(impacts_df, product_id="P001")
        fig5.show()

        print("\nVisualizing correlation between impact categories...")
        fig6 = visualizer.plot_impact_correlation(impacts_df)
        fig6.show()

    except Exception as e:
        print(f"Visualization failed: {e}")

if __name__ == "__main__":
    main()
