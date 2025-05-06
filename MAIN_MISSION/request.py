import requests
import os
import time
from urllib.parse import urljoin

# --- Configuration ---
# Replace with the actual IP address of the source computer
#SERVER_IP = "192.168.30.215" # inet sur commande: ip a dans le terminal de RbP
SERVER_IP = 'zenith.local'
SERVER_PORT = 8000
BASE_URL = f"http://{SERVER_IP}:{SERVER_PORT}/"

# List of specific files to download from the server
FILES_TO_DOWNLOAD = [
    "stock_centroids.csv"
]

# Local directory on the ground station to save downloaded files
mission_dir = "/home/colin/AEAC-2025-Mission-1"

csv_dir = os.path.join(mission_dir, "MAIN_MISSION", "csvs")

# --- Script Logic ---

def download_file(file_url, local_filename):
    """Downloads a single file from the server."""
    print(f"Attempting to download {file_url} to {local_filename}...")
    try:
        # Make the request, stream=True is important for large files
        with requests.get(file_url, stream=True, timeout=30) as r:
            r.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            # Open the local file in binary write mode
            with open(local_filename, 'wb') as f:
                # Download in chunks
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Successfully downloaded {local_filename}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Could not connect to the server at {BASE_URL}. {e}")
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out for {file_url}")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP Error for {file_url}: {e.response.status_code} {e.response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: An unexpected error occurred during download: {e}")
    except OSError as e:
        print(f"Error: Could not write file {local_filename}. {e}")
    return False

def main():
    """Main function to orchestrate the download."""
    # Create the local download directory if it doesn't exist
    #os.makedirs(csv_dir, exist_ok=True)
    #print(f"Ensured download directory exists: {csv_dir}")

    successful_downloads = 0
    for filename in FILES_TO_DOWNLOAD:
        file_url = urljoin(BASE_URL, filename) # Construct full URL
        # Prepend the download directory path to the filename
        local_path = os.path.join(csv_dir, filename)

        if download_file(file_url, local_path):
            successful_downloads += 1
        else:
            print(f"Failed to download {filename}.")
        time.sleep(1) # Small delay between requests

    print("-" * 20)
    print(f"Download process finished.")
    print(f"Successfully downloaded {successful_downloads} out of {len(FILES_TO_DOWNLOAD)} files.")

while True:
    main()
    time.sleep(5)