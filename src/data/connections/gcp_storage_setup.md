Absolutely! Here's a **step-by-step guide from scratch** to set up **Google Cloud Storage access** using a **service account** and use it in your **Python project** to fetch data (just like you were doing with S3).

---

# ✅ GCP + Python Setup for Data Ingestion from Google Cloud Storage (GCS)

---

## 🧩 Step 1: Set Up Your Google Cloud Project

1. Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. In the top navbar, create or select a project (e.g., `insurance-mlops`).

---

## 🔐 Step 2: Create a Service Account

1. Open [IAM & Admin → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click **“Create Service Account”**
3. Fill in:

   * **Name**: `mlops-access`
   * **ID**: auto-filled (e.g., `mlops-access@your-project-id.iam.gserviceaccount.com`)
4. Click **Continue**

---

## 🛡️ Step 3: Grant GCS Permissions

On the next screen (step 2 of 3):

1. Under **"Grant this service account access to project"**:

   * Click **"Select a role"**
   * Search for and select: ✅ `Storage Object Viewer`
2. Click **Continue**, then **Done**

---

## 📁 Step 4: Create & Download JSON Key

1. After the service account is created, click on it in the list
2. Go to the **"Keys"** tab
3. Click **“Add Key” > “Create New Key”**
4. Choose **JSON**, then click **Create**

> 🔽 Your browser will download a `.json` key file — this is your **credentials file**.

---

## ⚙️ Step 5: Enable Cloud Storage API

1. Go to [Cloud Storage API](https://console.cloud.google.com/apis/library/storage.googleapis.com)
2. Click **Enable**

---

## 🌐 Step 6: Create a Storage Bucket & Upload a File

1. Go to [Cloud Storage](https://console.cloud.google.com/storage/browser)
2. Click **“Create Bucket”**

   * Give it a globally unique name, like `insurance-mlops-data`
   * Leave other settings as default and click **Create**
3. Click the bucket and upload your CSV file (e.g., `data.csv`)

---

## 🧪 Step 7: Set Up Python Environment Locally

1. In your project folder:

```bash
python -m venv venv
.\venv\Scripts\activate  # For Windows
```

2. Install required library:

```bash
pip install google-cloud-storage pandas
```

3. Set environment variable so Python can use your key file:

In **PowerShell**:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Path\To\your-service-account.json"
```

---

## 🧑‍💻 Step 8: Python Script to Read from GCS

```python
from google.cloud import storage
import pandas as pd
from io import StringIO
from src.logger import logging  # if using your own logger

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

# Example usage
# BUCKET_NAME = "insurance-mlops-data"
# FILE_KEY = "data.csv"
# ingestion = gcs_operations(BUCKET_NAME)
# df = ingestion.fetch_file_from_gcs(FILE_KEY)
```

---

## ✅ Step 9: Run Your Script

```bash
python src/data/data_ingestion.py
```

You should see logs showing successful download from GCS and dataframe creation.

---

## ✅ Summary

| Step | Task                                          |
| ---- | --------------------------------------------- |
| 1    | Create GCP project                            |
| 2    | Create service account                        |
| 3    | Grant `Storage Object Viewer` role            |
| 4    | Download JSON key                             |
| 5    | Enable Cloud Storage API                      |
| 6    | Create bucket & upload data                   |
| 7    | Setup Python + install `google-cloud-storage` |
| 8    | Write code to read from GCS                   |
| 9    | Run and verify                                |

---

Let me know:

* if you want help uploading files to GCS too
* if you want to run this from **Colab**, **Vertex AI**, or **CI/CD pipelines**

I can tailor the next steps to your use case.
