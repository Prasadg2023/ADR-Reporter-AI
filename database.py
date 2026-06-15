import mysql.connector
from mysql.connector import Error
import sqlite3
import streamlit as st
import os

# Absolute path for SQLite database to keep data storage location consistent
DB_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(DB_DIR, "adr_reports.db")

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
_db_initialized = False

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
    global _db_initialized
    if _db_initialized:
        return
    check_mysql_available()
    
    if _use_sqlite:
        conn = sqlite3.connect(SQLITE_DB_PATH)
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
            
            # Migration to add pdf_data column if it doesn't exist
            cursor.execute("PRAGMA table_info(reports)")
            columns = [info[1] for info in cursor.fetchall()]
            if "pdf_data" not in columns:
                cursor.execute("ALTER TABLE reports ADD COLUMN pdf_data BLOB")
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
            _db_initialized = True
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
            
            # Migration to add pdf_data column if it doesn't exist
            cursor.execute("SHOW COLUMNS FROM reports LIKE 'pdf_data'")
            result = cursor.fetchone()
            if not result:
                cursor.execute("ALTER TABLE reports ADD COLUMN pdf_data LONGBLOB")
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
            _db_initialized = True
        except Error as e:
            st.error(f"Error initializing MySQL database: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_report(report_data):
    """Inserts a single report into the database and generates/stores the associated PDF."""
    init_db()
    
    fields = [
        "final_drug_category", "patient_name", "patient_email", "patient_mobile",
        "age", "gender", "weight_kg", "drug_name", "indication",
        "medicine_start_date", "medicine_stop_date", "reaction_start_date", "reaction_end_date",
        "reaction_description", "drug_category_manual", "route_of_administration", "strength",
        "frequency", "batch_number", "expiry_date", "action_taken", "physician_name", "physician_contact"
    ]
    values = tuple(report_data.get(field, None) for field in fields)
    
    if _use_sqlite:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(fields))
        columns = ", ".join(fields)
        insert_query = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(insert_query, values)
            report_id = cursor.lastrowid
            
            # Fetch back row to get generated/default fields (like submission_timestamp)
            cursor.execute("SELECT * FROM reports WHERE report_id = ?", (report_id,))
            row = cursor.fetchone()
            if row:
                row_dict = dict(row)
                from utils import generate_report_pdf
                try:
                    pdf_path = generate_report_pdf(row_dict)
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    cursor.execute("UPDATE reports SET pdf_data = ? WHERE report_id = ?", (pdf_bytes, report_id))
                    try:
                        os.remove(pdf_path)
                    except Exception:
                        pass
                except Exception as pdf_err:
                    st.error(f"Error generating PDF during insert: {pdf_err}")
                    
            conn.commit()
            try:
                st.cache_data.clear()
            except Exception:
                pass
            return True
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            import traceback
            try:
                with open("insert_error.log", "w") as err_f:
                    traceback.print_exc(file=err_f)
            except Exception:
                pass
            st.error(f"Error inserting report to SQLite: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_connection()
        if conn is None:
            return False
            
        cursor = conn.cursor(dictionary=True)
        placeholders = ", ".join(["%s"] * len(fields))
        columns = ", ".join(fields)
        insert_query = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(insert_query, values)
            report_id = cursor.lastrowid
            
            # Fetch back row
            cursor.execute("SELECT * FROM reports WHERE report_id = %s", (report_id,))
            row_dict = cursor.fetchone()
            if row_dict:
                from utils import generate_report_pdf
                try:
                    pdf_path = generate_report_pdf(row_dict)
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    cursor.execute("UPDATE reports SET pdf_data = %s WHERE report_id = %s", (pdf_bytes, report_id))
                    try:
                        os.remove(pdf_path)
                    except Exception:
                        pass
                except Exception as pdf_err:
                    st.error(f"Error generating PDF during insert: {pdf_err}")
            
            conn.commit()
            try:
                st.cache_data.clear()
            except Exception:
                pass
            return True
        except Error as e:
            try:
                conn.rollback()
            except Exception:
                pass
            import traceback
            try:
                with open("insert_error_mysql.log", "w") as err_f:
                    traceback.print_exc(file=err_f)
            except Exception:
                pass
            st.error(f"Error inserting report to MySQL: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def get_all_reports():
    """Fetches all reports from the database, excluding pdf_data for performance."""
    init_db()
    
    fields = [
        "report_id", "submission_timestamp", "final_drug_category", "patient_name", "patient_email",
        "patient_mobile", "age", "gender", "weight_kg", "drug_name", "indication",
        "medicine_start_date", "medicine_stop_date", "reaction_start_date", "reaction_end_date",
        "reaction_description", "drug_category_manual", "route_of_administration", "strength",
        "frequency", "batch_number", "expiry_date", "action_taken", "physician_name", "physician_contact"
    ]
    columns_str = ", ".join(fields)
    
    if _use_sqlite:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT {columns_str} FROM reports ORDER BY report_id ASC")
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
            cursor.execute(f"SELECT {columns_str} FROM reports ORDER BY report_id ASC")
            result = cursor.fetchall()
            return result
        except Error as e:
            st.error(f"Error fetching reports from MySQL: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

def get_report_pdf(report_id):
    """Fetches the PDF bytes for a report. Dynamically generates and stores it if missing."""
    init_db()
    
    pdf_bytes = None
    row_data = None
    
    if _use_sqlite:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM reports WHERE report_id = ?", (report_id,))
            row = cursor.fetchone()
            if row:
                row_data = dict(row)
                pdf_bytes = row_data.get('pdf_data')
        except Exception as e:
            st.error(f"Error fetching PDF from SQLite: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_connection()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM reports WHERE report_id = %s", (report_id,))
                row = cursor.fetchone()
                if row:
                    row_data = row
                    pdf_bytes = row_data.get('pdf_data')
            except Error as e:
                st.error(f"Error fetching PDF from MySQL: {e}")
            finally:
                cursor.close()
                conn.close()
                
    if pdf_bytes:
        return pdf_bytes
        
    if row_data:
        # Generate the PDF on the fly and save it to the database
        from utils import generate_report_pdf
        try:
            row_data_copy = row_data.copy()
            if 'pdf_data' in row_data_copy:
                del row_data_copy['pdf_data']
            pdf_path = generate_report_pdf(row_data_copy)
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            
            # Save pdf_bytes to DB
            if _use_sqlite:
                conn = sqlite3.connect(SQLITE_DB_PATH)
                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE reports SET pdf_data = ? WHERE report_id = ?", (pdf_bytes, report_id))
                    conn.commit()
                except Exception as e:
                    st.error(f"Error saving generated PDF to SQLite: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                conn = get_connection()
                if conn is not None:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("UPDATE reports SET pdf_data = %s WHERE report_id = %s", (pdf_bytes, report_id))
                        conn.commit()
                    except Error as e:
                        st.error(f"Error saving generated PDF to MySQL: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                        
            # Clean up temp file
            try:
                os.remove(pdf_path)
            except Exception:
                pass
            return pdf_bytes
        except Exception as e:
            st.error(f"Error generating PDF dynamically: {e}")
            
    return None

def delete_report(report_id):
    """Deletes a report from the database by report_id."""
    init_db()
    
    if _use_sqlite:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM reports WHERE report_id = ?", (report_id,))
            conn.commit()
            try:
                st.cache_data.clear()
            except Exception:
                pass
            return True
        except Exception as e:
            st.error(f"Error deleting report from SQLite: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_connection()
        if conn is None:
            return False
            
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM reports WHERE report_id = %s", (report_id,))
            conn.commit()
            try:
                st.cache_data.clear()
            except Exception:
                pass
            return True
        except Error as e:
            st.error(f"Error deleting report from MySQL: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
