# main.py – Entry point for the Life‑Cycle Assessment (LCA) tool
# ===============================================================
"""

1. Load and (optionally) pre‑process product data
2. Validate the dataset
3. Compute environmental impacts
4. Visualise the outcomes
5. Persist aggregated results

Run `python main.py --help` to see all CLI options.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# --- Project modules --------------------------------------------------------
from src.data_input import DataInput
from src.calculations import LCACalculator
from src.utils import save_results
from src.visualization import LCAVisualizer

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def parse_cli_args() -> argparse.Namespace:
    """Parse command‑line parameters and return the populated namespace."""
    parser = argparse.ArgumentParser(
        description="Run a full Life‑Cycle Assessment workflow on a dataset."
    )
    parser.add_argument(
        "--product-data",
        type=Path,
        default=Path("data/raw/sample_data.csv"),
        help="Path to the product inventory file (CSV, XLSX or JSON).",
    )
    parser.add_argument(
        "--impact-factors",
        type=Path,
        default=Path("data/raw/impact_factors.json"),
        help="JSON file containing impact factors (material × stage).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        help="Directory where derived artefacts (CSV, figures) will be stored.",
    )
    parser.add_argument(
        "--backend",
        default="TkAgg",
        choices=matplotlib.rcsetup.all_backends,
        help="Matplotlib backend to use for rendering the figures.",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Generate figures but do *not* display the GUI window (useful on CI).",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with a sensible format."""
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# ---------------------------------------------------------------------------
# Core workflow functions
# ---------------------------------------------------------------------------

def load_and_prepare_data(data_path: Path) -> pd.DataFrame | None:
    """Load product data and perform minimal preprocessing.

    Returns a *validated* DataFrame or *None* if validation fails.
    """
    di = DataInput()
    df = di.read_data(data_path)

    # Example preprocessing: ensure End‑of‑Life rates sum to 1, others to 0/1/0
    lifecycle_mask = df["life_cycle_stage"].str.strip().str.lower() != "end-of-life"
    df.loc[lifecycle_mask, ["recycling_rate", "landfill_rate", "incineration_rate"]] = (
        0.0,
        1.0,
        0.0,
    )

    if not di.validate_data(df):
        logging.error("Dataset validation failed – aborting workflow.")
        return None

    return df


def compute_impacts(df: pd.DataFrame, factors_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute line‑item and product‑level environmental impacts."""
    calc = LCACalculator(impact_factors_path=factors_path)
    impacts = calc.calculate_impacts(df)
    totals = calc.calculate_total_impacts(impacts)
    return impacts, totals


def visualise(impacts: pd.DataFrame, show_gui: bool = True) -> None:
    """Render a suite of diagnostic figures for the given impacts DataFrame."""
    vis = LCAVisualizer()

    logging.info("Drawing impact breakdown pie‑chart.")
    vis.plot_impact_breakdown(impacts, "carbon_impact", "material_type")
    if show_gui:
        plt.show()

    logging.info("Drawing life‑cycle bar‑chart for the first product in the set.")
    first_product = impacts["product_id"].iloc[0]
    vis.plot_life_cycle_impacts(impacts, first_product)
    if show_gui:
        plt.show()

    logging.info("Drawing radar chart comparing all products.")
    unique_products = impacts["product_id"].unique().tolist()
    vis.plot_product_comparison(impacts, unique_products)
    if show_gui:
        plt.show()

    logging.info("Drawing impact‑category correlation heatmap.")
    vis.plot_impact_correlation(impacts)
    if show_gui:
        plt.show()


# ---------------------------------------------------------------------------
# Entry‑point
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_cli_args()

    # The backend must be set *before* importing pyplot.
    matplotlib.use(args.backend)

    configure_logging()

    logging.info("Starting Life‑Cycle Assessment workflow …")

    # 1) Load & validate -----------------------------------------------------
    logging.info("Loading product data from '%s'.", args.product_data)
    product_df = load_and_prepare_data(args.product_data)
    if product_df is None:
        return  # validation failed
    logging.info("Product dataset loaded (shape = %s).", product_df.shape)

    # 2) Compute impacts -----------------------------------------------------
    logging.info("Computing environmental impacts …")
    impacts_df, totals_df = compute_impacts(product_df, args.impact_factors)

    # 3) Visualise -----------------------------------------------------------
    visualise(impacts_df, show_gui=not args.no_show)

    # 4) Persist totals ------------------------------------------------------
    args.output_dir.mkdir(exist_ok=True, parents=True)
    output_file = args.output_dir / "total_impact_results.csv"
    save_results(totals_df, output_file, format="csv")
    logging.info("Aggregated results written to '%s'.", output_file)

    logging.info("Workflow completed successfully.")


if __name__ == "__main__":
    main()
