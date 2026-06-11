import mysql.connector
from mysql.connector import Error
import streamlit as st
from datetime import datetime

# Database Configuration
# These can be changed by the user in MySQL Workbench if needed
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root" # Updated as requested
DB_NAME = "adr_reports_db"

def get_connection(use_db=True):
    """Establishes a connection to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME if use_db else None
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initializes the database and creates the reports table if it doesn't exist."""
    conn = get_connection(use_db=False)
    if conn is None:
        return

    cursor = conn.cursor()
    
    # Create Database
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # Create Table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS reports (
            report_id INT AUTO_INCREMENT PRIMARY KEY,
            submission_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            final_drug_category VARCHAR(100),
            patient_name VARCHAR(255),
            patient_email VARCHAR(255),
            patient_mobile VARCHAR(50),
            age INT,
            gender VARCHAR(50),
            weight_kg VARCHAR(50),
            drug_name VARCHAR(255),
            indication TEXT,
            medicine_start_date VARCHAR(100),
            medicine_stop_date VARCHAR(100),
            reaction_start_date VARCHAR(100),
            reaction_end_date VARCHAR(100),
            reaction_description TEXT,
            drug_category_manual VARCHAR(100),
            route_of_administration VARCHAR(255),
            strength VARCHAR(100),
            frequency VARCHAR(100),
            batch_number VARCHAR(100),
            expiry_date VARCHAR(100),
            action_taken TEXT,
            physician_name VARCHAR(255),
            physician_contact VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        
        # Migrate/normalize older drug category values to match new unified therapeutic classes
        migrations = [
            "UPDATE reports SET final_drug_category = 'NSAIDs' WHERE LOWER(final_drug_category) IN ('nsaid', 'nsaid / analgesic', 'nsaid/analgesic', 'nsaids')",
            "UPDATE reports SET final_drug_category = 'Antibiotics' WHERE LOWER(final_drug_category) IN ('antibiotic', 'antibiotics')",
            "UPDATE reports SET final_drug_category = 'Antihistamines' WHERE LOWER(final_drug_category) IN ('antiallergic / antihistamine', 'antiallergic/antihistamine', 'antihistamine', 'antihistamines')",
            "UPDATE reports SET final_drug_category = 'Antidiabetics' WHERE LOWER(final_drug_category) IN ('antidiabetic', 'antidiabetics')",
            "UPDATE reports SET final_drug_category = 'Antihypertensives' WHERE LOWER(final_drug_category) IN ('antihypertensive', 'antihypertensives')",
            "UPDATE reports SET final_drug_category = 'Beta-blockers' WHERE LOWER(final_drug_category) IN ('beta-blocker', 'beta-blockers', 'betabloker', 'betablocker')",
            "UPDATE reports SET final_drug_category = 'Calcium Channel Blockers' WHERE LOWER(final_drug_category) IN ('calcium channel blocker', 'calcium channel blockers')",
            "UPDATE reports SET final_drug_category = 'ACE Inhibitors' WHERE LOWER(final_drug_category) IN ('ace inhibitor', 'ace inhibitors')",
            "UPDATE reports SET final_drug_category = 'Angiotensin Receptor Blockers (ARBs)' WHERE LOWER(final_drug_category) IN ('angiotensin receptor blocker (arbs)', 'angiotensin receptor blockers', 'arb', 'arbs')",
            "UPDATE reports SET final_drug_category = 'Diuretics' WHERE LOWER(final_drug_category) IN ('diuretic', 'diuretics')",
            "UPDATE reports SET final_drug_category = 'Statins / Lipid-lowering Drugs' WHERE LOWER(final_drug_category) IN ('statin', 'statins', 'statin / lipid-lowering drugs', 'statin/lipid-lowering drugs', 'statins / lipid-lowering drugs', 'statins/lipid-lowering drugs')",
            "UPDATE reports SET final_drug_category = 'Benzodiazepines' WHERE LOWER(final_drug_category) IN ('benzodiazepine', 'benzodiazepines')",
            "UPDATE reports SET final_drug_category = 'Antipyretics' WHERE LOWER(final_drug_category) IN ('antipyretic', 'antipyretics')",
            "UPDATE reports SET final_drug_category = 'Others' WHERE LOWER(final_drug_category) IN ('other', 'others')"
        ]
        for query in migrations:
            try:
                cursor.execute(query)
            except Error:
                pass
        conn.commit()
    except Error as e:
        st.error(f"Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()

def insert_report(report_data):
    """Inserts a single report into the database."""
    conn = get_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    # Prepare query
    fields = [
        "final_drug_category", "patient_name", "patient_email", "patient_mobile",
        "age", "gender", "weight_kg", "drug_name", "indication",
        "medicine_start_date", "medicine_stop_date", "reaction_start_date", "reaction_end_date",
        "reaction_description", "drug_category_manual", "route_of_administration", "strength",
        "frequency", "batch_number", "expiry_date", "action_taken", "physician_name", "physician_contact"
    ]
    
    placeholders = ", ".join(["%s"] * len(fields))
    columns = ", ".join(fields)
    
    insert_query = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
    
    # Extract values in correct order
    values = tuple(report_data.get(field, None) for field in fields)
    
    try:
        cursor.execute(insert_query, values)
        conn.commit()
        return True
    except Error as e:
        st.error(f"Error inserting report: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_reports():
    """Fetches all reports from the database."""
    conn = get_connection()
    if conn is None:
        return []
        
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM reports ORDER BY report_id ASC")
        result = cursor.fetchall()
        return result
    except Error as e:
        st.error(f"Error fetching reports: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
