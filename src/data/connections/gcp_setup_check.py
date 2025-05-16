from google.cloud import storage

def list_buckets():
    try:
        client = storage.Client()
        buckets = list(client.list_buckets())
        print("✅ GCP authentication successful.")
        print("Found buckets:")
        for bucket in buckets:
            print(f" - {bucket.name}")
    except Exception as e:
        print(f"❌ Authentication failed or permission error: {e}")

if __name__ == "__main__":
    list_buckets()
