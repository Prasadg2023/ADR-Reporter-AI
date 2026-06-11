import mysql.connector
from mysql.connector import Error
import sqlite3
import streamlit as st
import os

# Database Configuration
# These can be changed by the user in MySQL Workbench or Streamlit Secrets
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "adr_reports_db"

# Check if Streamlit Secrets are available for cloud deployment database configs
try:
    if hasattr(st, "secrets") and "database" in st.secrets:
        DB_HOST = st.secrets["database"].get("host", DB_HOST)
        DB_USER = st.secrets["database"].get("user", DB_USER)
        DB_PASSWORD = st.secrets["database"].get("password", DB_PASSWORD)
        DB_NAME = st.secrets["database"].get("database", DB_NAME)
except Exception:
    # Safe to ignore if not running in Streamlit environment with configured secrets
    pass

_use_sqlite = False

def check_mysql_available():
    """Pings the MySQL server to detect if we should fallback to SQLite."""
    global _use_sqlite
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=2
        )
        connection.close()
        _use_sqlite = False
        return True
    except Exception:
        # If MySQL is not running (e.g. Streamlit Cloud, XAMPP turned off), use SQLite fallback
        _use_sqlite = True
        return False

def get_connection(use_db=True):
    """Establishes a connection to the MySQL server (only used in MySQL mode)."""
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
    check_mysql_available()
    
    if _use_sqlite:
        conn = sqlite3.connect("adr_reports.db")
        cursor = conn.cursor()
        try:
            # Create Table in SQLite (SQLite uses INTEGER PRIMARY KEY for auto-increment)
            create_table_query = """
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                submission_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                final_drug_category TEXT,
                patient_name TEXT,
                patient_email TEXT,
                patient_mobile TEXT,
                age INTEGER,
                gender TEXT,
                weight_kg TEXT,
                drug_name TEXT,
                indication TEXT,
                medicine_start_date TEXT,
                medicine_stop_date TEXT,
                reaction_start_date TEXT,
                reaction_end_date TEXT,
                reaction_description TEXT,
                drug_category_manual TEXT,
                route_of_administration TEXT,
                strength TEXT,
                frequency TEXT,
                batch_number TEXT,
                expiry_date TEXT,
                action_taken TEXT,
                physician_name TEXT,
                physician_contact TEXT
            )
            """
            cursor.execute(create_table_query)
            conn.commit()
            
            # Clean up categories / run migrations in SQLite
            migrations = [
                "UPDATE reports SET final_drug_category = 'Beta-blockers' WHERE LOWER(final_drug_category) IN ('beta-blocker', 'beta-blockers', 'betabloker', 'betablocker')",
                "UPDATE reports SET final_drug_category = 'NSAIDs' WHERE LOWER(final_drug_category) IN ('nsaid', 'nsaid / analgesic', 'nsaid/analgesic', 'nsaids')",
                "UPDATE reports SET final_drug_category = 'Antibiotics' WHERE LOWER(final_drug_category) IN ('antibiotic', 'antibiotics')",
                "UPDATE reports SET final_drug_category = 'Antihistamines' WHERE LOWER(final_drug_category) IN ('antiallergic / antihistamine', 'antiallergic/antihistamine', 'antihistamine', 'antihistamines')",
                "UPDATE reports SET final_drug_category = 'Antidiabetics' WHERE LOWER(final_drug_category) IN ('antidiabetic', 'antidiabetics')",
                "UPDATE reports SET final_drug_category = 'Antihypertensives' WHERE LOWER(final_drug_category) IN ('antihypertensive', 'antihypertensives')",
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
                except Exception:
                    pass
            conn.commit()
        except Exception as e:
            st.error(f"Error initializing SQLite DB: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        # MySQL Initialization
        conn = get_connection(use_db=False)
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cursor.execute(f"USE {DB_NAME}")
            
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
            
            migrations = [
                "UPDATE reports SET final_drug_category = 'Beta-blockers' WHERE LOWER(final_drug_category) IN ('beta-blocker', 'beta-blockers', 'betabloker', 'betablocker')",
                "UPDATE reports SET final_drug_category = 'NSAIDs' WHERE LOWER(final_drug_category) IN ('nsaid', 'nsaid / analgesic', 'nsaid/analgesic', 'nsaids')",
                "UPDATE reports SET final_drug_category = 'Antibiotics' WHERE LOWER(final_drug_category) IN ('antibiotic', 'antibiotics')",
                "UPDATE reports SET final_drug_category = 'Antihistamines' WHERE LOWER(final_drug_category) IN ('antiallergic / antihistamine', 'antiallergic/antihistamine', 'antihistamine', 'antihistamines')",
                "UPDATE reports SET final_drug_category = 'Antidiabetics' WHERE LOWER(final_drug_category) IN ('antidiabetic', 'antidiabetics')",
                "UPDATE reports SET final_drug_category = 'Antihypertensives' WHERE LOWER(final_drug_category) IN ('antihypertensive', 'antihypertensives')",
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
            st.error(f"Error initializing MySQL database: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_report(report_data):
    """Inserts a single report into the database."""
    check_mysql_available()
    
    fields = [
        "final_drug_category", "patient_name", "patient_email", "patient_mobile",
        "age", "gender", "weight_kg", "drug_name", "indication",
        "medicine_start_date", "medicine_stop_date", "reaction_start_date", "reaction_end_date",
        "reaction_description", "drug_category_manual", "route_of_administration", "strength",
        "frequency", "batch_number", "expiry_date", "action_taken", "physician_name", "physician_contact"
    ]
    values = tuple(report_data.get(field, None) for field in fields)
    
    if _use_sqlite:
        conn = sqlite3.connect("adr_reports.db")
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(fields))
        columns = ", ".join(fields)
        insert_query = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(insert_query, values)
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Error inserting report to SQLite: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_connection()
        if conn is None:
            return False
            
        cursor = conn.cursor()
        placeholders = ", ".join(["%s"] * len(fields))
        columns = ", ".join(fields)
        insert_query = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(insert_query, values)
            conn.commit()
            return True
        except Error as e:
            st.error(f"Error inserting report to MySQL: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def get_all_reports():
    """Fetches all reports from the database."""
    check_mysql_available()
    
    if _use_sqlite:
        conn = sqlite3.connect("adr_reports.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM reports ORDER BY report_id ASC")
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            return result
        except Exception as e:
            st.error(f"Error fetching reports from SQLite: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_connection()
        if conn is None:
            return []
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM reports ORDER BY report_id ASC")
            result = cursor.fetchall()
            return result
        except Error as e:
            st.error(f"Error fetching reports from MySQL: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
