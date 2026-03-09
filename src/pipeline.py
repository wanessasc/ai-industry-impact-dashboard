from src.data_loader import load_raw_data, save_processed_data
from src.preprocessing import clean_dataset


def run_pipeline() -> None:
    raw_df = load_raw_data()
    processed_df = clean_dataset(raw_df)
    output_path = save_processed_data(processed_df)
    print(f"Processed data saved to: {output_path}")
    print(f"Rows: {processed_df.shape[0]}, Columns: {processed_df.shape[1]}")


if __name__ == "__main__":
    run_pipeline()
