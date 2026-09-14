# flows/metrics_flow.py
from prefect import flow

from tasks.sp_migration import extract_transactions, load_summaries, transform_metrics


@flow(name="sp-migration-flow")
def run_sp_conversion():
    raw_df = extract_transactions()
    transformed_df = transform_metrics(raw_df)
    load_summaries(transformed_df)

if __name__ == "__main__":
    run_sp_conversion()
