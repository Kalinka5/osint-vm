from azure.storage.blob import BlobServiceClient

import sqlite3

import requests
from urllib.parse import urljoin, urlparse

from concurrent.futures import ThreadPoolExecutor

from io import BytesIO
from PIL import Image

import hashlib

import time


# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=osintwebstorage;AccountKey=TgYesm49TbHEI0EqeUjXVShCui7ImRuE18pfbBiY2tfW6XteK//QymqCspk5/PBmdGceMO9LKcYI+AStcAq55A==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "companies-images"

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


def initialize_database(db_path):
    """Ensure the database schema includes the necessary tables and columns."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create `company_images` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_images (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            image_url TEXT NOT NULL,
            image_hash TEXT UNIQUE NOT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )
    """)

    # Add `image_id` column to `companies` table if not exists
    cursor.execute("PRAGMA table_info(companies)")
    columns = [column[1] for column in cursor.fetchall()]
    if "image_id" not in columns:
        cursor.execute(
            "ALTER TABLE companies ADD COLUMN image_id INTEGER REFERENCES company_images(id)")

    conn.commit()
    conn.close()


def get_favicon_url(domain):
    """Retrieve the favicon URL from a website's HTML."""
    try:
        response = requests.get(domain, timeout=20)
        response.raise_for_status()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Search for the favicon link in the HTML
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())

        if icon_link and 'href' in icon_link.attrs:
            return urljoin(domain, icon_link['href'])
        else:
            # Fallback to common favicon path
            parsed_url = urlparse(domain)
            return f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
    except Exception as e:
        print(f"Error retrieving favicon for {domain}: {e}")
        return None


def calculate_image_hash(image_data):
    """Calculate a unique hash for the image data."""
    return hashlib.sha256(image_data).hexdigest()


def download_and_convert_favicon(favicon_url):
    """Download the favicon and convert it to PNG format."""
    try:
        response = requests.get(favicon_url, timeout=10, stream=True)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGBA")

        png_buffer = BytesIO()
        img.save(png_buffer, format="PNG")

        return png_buffer.getvalue()
    except Exception as e:
        print(f"Error downloading or converting favicon from {
              favicon_url}: {e}")
        return None


def upload_favicon_to_azure(favicon_data, company_id):
    """Upload the favicon image to Azure Blob Storage."""
    try:
        png_buffer = BytesIO(favicon_data)
        blob_name = f"{company_id}.png"

        # Upload to Azure Blob Storage
        container_client.upload_blob(blob_name, png_buffer, overwrite=True)

        # Generate and return the Blob URL
        return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
    except Exception as e:
        print(f"Error uploading favicon to Azure for company ID {
              company_id}: {e}")
        return None


def process_company(company, db_path):
    """Process a single company to download favicon and update the database."""
    company_id, website = company
    print(f"Processing website: {website}")
    favicon_url = get_favicon_url(website)

    if not favicon_url:
        print(f"No valid favicon URL for website: {website}")
        return

    favicon_data = download_and_convert_favicon(favicon_url)

    if favicon_data:
        # Calculate the hash of the favicon
        image_hash = calculate_image_hash(favicon_data)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Check if the hash already exists in `company_images`
            cursor.execute(
                "SELECT id, image_url FROM company_images WHERE image_hash = ?", (image_hash,))
            existing_image = cursor.fetchone()

            if existing_image:
                # Reuse the existing image
                image_id, image_url = existing_image
                print(f"Reusing existing favicon for company ID {
                      company_id}, URL: {image_url}.")
            else:
                # Upload favicon to Azure Blob Storage
                blob_url = upload_favicon_to_azure(favicon_data, company_id)
                if not blob_url:
                    print(f"Failed to upload favicon for website: {website}.")
                    return

                # Insert the new image into `company_images`
                cursor.execute(
                    "INSERT INTO company_images (company_id, image_url, image_hash) VALUES (?, ?, ?)",
                    (company_id, blob_url, image_hash)
                )
                image_id = cursor.lastrowid
                print(f"Favicon added for company ID {
                      company_id} with URL: {blob_url}.")

            # Update the `companies` table with the new `image_id`
            cursor.execute(
                "UPDATE companies SET image_id = ? WHERE id = ?", (
                    image_id, company_id)
            )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating database for company ID {company_id}: {e}")
    else:
        print(f"Failed to download favicon for website: {website}.")


def update_favicons_in_db(db_path, max_workers=10):
    """Read company data from the SQLite database and update favicons."""
    initialize_database(db_path)  # Ensure the database schema is ready

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch companies with website
        cursor.execute("SELECT id, website FROM companies")
        companies = cursor.fetchall()
        conn.close()

        print(f"Found {len(companies)} companies to process.")
        time.sleep(5)

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(lambda company: process_company(
                company, db_path), companies)

        print("Database update complete.")
    except Exception as e:
        print(f"Error updating favicons in database: {e}")


# Example usage
if __name__ == "__main__":
    database_path = "backend/companies.db"  # Path to your SQLite database
    # Adjust max_workers as needed based on your system resources
    update_favicons_in_db(database_path, max_workers=50)
