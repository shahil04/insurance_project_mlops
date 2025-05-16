create github

✅ Option 1: Remove the Last Commit but Keep the Changes (Uncommit)
This is useful if you accidentally committed something (like a secret) and want to revise it:


git reset --soft HEAD~1

dvc remote list

pip install dvc[gcs] google-cloud-storage
mlop4_bucket

 Run this:
bash
Copy
Edit
pip install dvc-gs
This will install the missing GCS plugin (dvc_gs), which is separate from dvc[gcs] in newer DVC versions.



==========================dvc add after all

Great — you want to configure **DVC remote storage on Google Cloud Storage (GCS)** instead of S3. Here's a step-by-step guide that **replaces S3 with GCS** for steps 23–27:

---

# ✅ Using GCS as DVC Remote Storage (S3 Equivalent)

---

## 🔧 Step 23: Create GCP Service Account & GCS Bucket

### 📌 A. Create a Service Account

1. Go to: [IAM & Admin → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click **Create Service Account**
3. Give it a name like `dvc-storage-access`
4. Click **Continue**
5. Assign role: `Storage Object Admin`
6. Click **Done**

---

### 📌 B. Create & Download JSON Key

1. Click on the newly created service account
2. Go to the **"Keys"** tab
3. Click **Add Key → Create new key → JSON**
4. Save the downloaded `.json` file securely

---

### 📌 C. Create a GCS Bucket

1. Go to: [Cloud Storage → Browser](https://console.cloud.google.com/storage/browser)
2. Click **Create bucket**
3. Name it uniquely (e.g., `insurance-mlops-dvc-store`)
4. Choose **Standard**, and **default settings**, then click **Create**

---

## 📦 Step 24: Install Required Packages

```bash
pip install dvc[gcs] google-cloud-storage
```

If you don’t have DVC already:

```bash
pip install dvc
```

---

## ❌ Step 25: (Optional) Remove Old Remotes

```bash
dvc remote list
dvc remote remove myremote  # if needed
```

---

## 🔑 Step 26: Set Google Cloud Credentials

Set the environment variable so DVC can authenticate:

### ✅ PowerShell / CMD (Windows):

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Path\To\your-service-account.json"
```

### ✅ Bash / Linux / Mac:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account.json"
```

> 🔁 You can also add it to your `.bashrc` or `.env` if you want to make it persistent.

---

## 📂 Step 27: Add GCS as DVC Remote Storage

```bash
dvc remote add -d myremote gs://insurance-mlops-dvc-store
```

> `-d` sets it as the default DVC remote.

---

## ✅ Test Your Setup

1. Track a file:

   ```bash
   dvc add data/train.csv
   ```
2. Commit changes:

   ```bash
   git add data/train.csv.dvc .gitignore
   git commit -m "Track training data with DVC"
   ```
3. Push data to GCS:

   ```bash
   dvc push
   ```

✅ If configured properly, DVC will upload your files to the GCS bucket.

---

## 🔐 Tip: Avoid Hardcoding Secrets

Instead of committing your JSON key:

* Add it to `.gitignore`:

  ```bash
  *.json
  ```

* Use environment variables only.

---

## ✅ Summary of GCS-Based DVC Setup

| Step                | Equivalent                                      |
| ------------------- | ----------------------------------------------- |
| IAM user (S3)       | GCP Service Account with `Storage Object Admin` |
| S3 bucket           | GCS bucket                                      |
| `aws configure`     | `GOOGLE_APPLICATION_CREDENTIALS` env variable   |
| `dvc remote add -d` | Same, but use `gs://bucket-name`                |

---

Let me know if you want to:

* Push entire datasets
* Set this up in CI/CD (GitHub Actions)
* Use `.env` or secret manager for auth

I can walk you through the next steps!
