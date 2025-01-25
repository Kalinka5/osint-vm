import sqlite3


def get_all_companies(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch companies with website
    cursor.execute("SELECT id, website FROM companies")
    companies = cursor.fetchall()
    conn.close()

    return companies


def get_companies_not_null(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch companies with website
    cursor.execute("SELECT id, website FROM companies WHERE image_id IS NULL")
    companies = cursor.fetchall()
    conn.close()

    return companies


def delete_duplicate_websites(db_path):
    """Delete all companies with repeated websites, keeping only one record per unique website."""
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Find duplicate websites and keep only the one with the lowest id
        cursor.execute("""
            DELETE FROM companies
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM companies
                GROUP BY website
            )
        """)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Duplicate websites have been removed. Only one record per website remains.")
    except Exception as e:
        print(f"Error deleting duplicate websites: {e}")


def drop_data_from_company_images(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Clear all data from 'company_images' table
    cursor.execute("DELETE FROM company_images;")
    conn.commit()

    print("Cleared all data from 'company_images' table.")

    # Close the connection
    conn.close()
