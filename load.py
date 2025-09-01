import os
import glob
from google.cloud import storage
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.environ["PROJECT_ID"]
GCP_BUCKET_NAME = os.environ["GCP_BUCKET_NAME"]
BIGQUERY_DATASET_ID = os.environ["BIGQUERY_DATASET_ID"]
BIGQUERY_TABLE_ID = os.environ["BIGQUERY_TABLE_ID"]

LOCAL_ORIGINAL_IMAGE_FOLDER = "./images/"
LOCAL_EDITED_IMAGE_FOLDER = "./edited_images/"
DATA_WITH_ID_PATH = "./data/FashionDataset_with_id.csv"

def upload_images_to_gcs(local_folder_path, gcs_destination_folder):

    try:
        storage_client = storage.Client(project = PROJECT_ID)
        bucket = storage_client.bucket(GCP_BUCKET_NAME)

        image_paths = glob.glob(os.path.join(local_folder_path, "*.jpg"))
        if not image_paths:
            print(f"No images found in {local_folder_path}.")

            return
        
        for image_path in image_paths:
            file_name = os.path.basename(image_path)
            blob = bucket.blob(os.path.join(gcs_destination_folder, file_name))
            blob.upload_from_filename(image_path)

        print(f"--- Successfully uploaded {len(image_paths)} images. ---")
    except Exception as e:
        print(f"An error occurred during GCS upload: {e}")

def load_csv_to_bigquery():

    try:
        bigquery_client = bigquery.Client(project = PROJECT_ID)
        table_ref = f"{BIGQUERY_DATASET_ID}.{BIGQUERY_TABLE_ID}"

        job_config = bigquery.LoadJobConfig(
            source_format = bigquery.SourceFormat.CSV,
            skip_leading_rows = 1,
            autodetect = True,
            write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,
            allow_quoted_newlines = True,
        )

        with open(DATA_WITH_ID_PATH, "rb") as source_file:
            load_job = bigquery_client.load_table_from_file(
                source_file, table_ref, job_config = job_config
            )

        load_job.result()  # Waits for the job to complete.

        destination_table = bigquery_client.get_table(table_ref)
        print(f"--- Successfully loaded {destination_table.num_rows} rows. ---")
    except Exception as e:
        print(f"An error occurred during BigQuery load: {e}")

def run_load_pipeline():
    upload_images_to_gcs(LOCAL_ORIGINAL_IMAGE_FOLDER, "original_images")
    upload_images_to_gcs(LOCAL_EDITED_IMAGE_FOLDER, "edited_images")
    load_csv_to_bigquery()