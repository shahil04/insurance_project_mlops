Great — let's **convert your S3-based `data_ingestion.py` to GCP (Google Cloud Storage)**.

---

### ✅ Goal:

Replace:

```python
s3 = s3_connection.s3_operations(...)
df = s3.fetch_file_from_s3("data.csv")
```

With:

```python
gcs = gcs_operations("your-bucket-name")
df = gcs.fetch_file_from_gcs("data.csv")
```

---

## ✅ Step-by-Step Conversion

Here’s the **modified full version** of your script with **GCS support**:

---

### 📄 `src/data/data_ingestion.py` (GCS version)

```python
import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import os
from sklearn.model_selection import train_test_split
import yaml
from src.logger import logging
from google.cloud import storage
from io import StringIO

# ========== GCS CONNECTION CLASS ==========
class gcs_operations:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        logging.info("Initialized GCS client.")

    def fetch_file_from_gcs(self, file_key):
        try:
            logging.info(f"Fetching '{file_key}' from GCS bucket '{self.bucket_name}'...")
            blob = self.bucket.blob(file_key)
            data = blob.download_as_text()
            df = pd.read_csv(StringIO(data))
            logging.info(f"Loaded '{file_key}' with {len(df)} records.")
            return df
        except Exception as e:
            logging.exception(f"❌ Failed to load '{file_key}': {e}")
            return None

# ========== PARAM LOADING ==========
def load_params(params_path: str) -> dict:
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logging.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logging.error('YAML error: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        raise

# ========== DATA LOADING ==========
def load_data(data_url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_url)
        logging.info('Data loaded from %s', data_url)
        return df
    except pd.errors.ParserError as e:
        logging.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the data: %s', e)
        raise

# ========== PREPROCESSING ==========
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logging.info("pre-processing...")
        final_df = df[df['sentiment'].isin(['positive', 'negative'])]
        final_df['sentiment'] = final_df['sentiment'].replace({'positive': 1, 'negative': 0})
        logging.info('Data preprocessing completed')
        return final_df
    except KeyError as e:
        logging.error('Missing column in the dataframe: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error during preprocessing: %s', e)
        raise

# ========== SAVE DATA ==========
def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logging.debug('Train and test data saved to %s', raw_data_path)
    except Exception as e:
        logging.error('Unexpected error occurred while saving the data: %s', e)
        raise

# ========== MAIN ==========
def main():
    try:
        # test_size = load_params('params.yaml')['data_ingestion']['test_size']
        test_size = 0.2

        # Replace with your actual GCS bucket and file
        BUCKET_NAME = "your-gcs-bucket-name"
        FILE_KEY = "data.csv"

        gcs = gcs_operations(bucket_name=BUCKET_NAME)
        df = gcs.fetch_file_from_gcs(FILE_KEY)

        if df is None:
            raise ValueError("Data loading failed from GCS.")

        final_df = preprocess_data(df)
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=42)
        save_data(train_data, test_data, data_path='./data')
    except Exception as e:
        logging.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
```

---

## ✅ Environment Setup Reminders

* Make sure your environment variable is set:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
```

* Install GCP libraries:

```bash
pip install google-cloud-storage pandas scikit-learn pyyaml
```

---

## ✅ Output

After running:

```bash
python src/data/data_ingestion.py
```

You should get:

* Logs showing GCS file fetched and processed
* Output files saved to:

  ```
  ./data/raw/train.csv
  ./data/raw/test.csv
  ```

---

Let me know if you want to:

* Upload processed files back to GCS
* Parameterize with `params.yaml`
* Use in a Vertex AI or CI/CD pipeline

I'm happy to walk through those next!
