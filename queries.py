import sqlite3
import re

DB_NAME = "clinic_database.db"

def execute_query(query, params=(), fetch=False, return_last_id=False):
    """Unified transaction pipeline that translates T-SQL server dialects for SQLite on the fly."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    results = None
    
    # Live Regex Dialect Translation Patches
    query_upper = query.upper()
    
    # 1. Convert SQL Server TOP 1 to SQLite LIMIT 1
    if "TOP 1" in query_upper:
        query = re.sub(r"SELECT\s+TOP\s+1\s+", "SELECT ", query, flags=re.IGNORECASE) + " LIMIT 1"
        
    # 2. Convert T-SQL GETDATE() to SQLite date('now')
    if "GETDATE()" in query_upper:
        query = query.replace("GETDATE()", "date('now')").replace("getdate()", "date('now')")
        
    # 3. Convert T-SQL DATEADD constructs into SQLite modifiers
    query = query.replace("DATEADD(MONTH, -1, GETDATE())", "date('now', '-1 month')")
    query = query.replace("DATEADD(month, -1, GETDATE())", "date('now', '-1 month')")
    query = query.replace("DATEADD(month, -1, date('now'))", "date('now', '-1 month')")
    
    # 4. Translate MONTH() and YEAR() functions into strftime string modifiers
    query = re.sub(r"MONTH\(([^)]+)\)", r"strftime('%m', \1)", query, flags=re.IGNORECASE)
    query = re.sub(r"YEAR\(([^)]+)\)", r"strftime('%Y', \1)", query, flags=re.IGNORECASE)

    try:
        cursor.execute(query, params)
        if fetch:
            results = cursor.fetchall()
        conn.commit()
        if return_last_id:
            results = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[SQL Error] In-Memory Compiler Exception: {e}")
    finally:
        conn.close()
    return results

def get_queries():
    """Returns your team's raw unedited T-SQL analysis blueprints."""
    return {
        # 1. أكتر فصيلة (Species) عملت زيارات طبية الشهر اللي فات
        "max_species_visits": """
            SELECT TOP 1 p.Species, COUNT(mv.VisitID) AS TotalVisits
            FROM Pet p JOIN MedicalVisit mv ON p.PetID = mv.PetID
            WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            GROUP BY p.Species ORDER BY TotalVisits DESC;
        """,
        # 2. العيادة اللي معملتش أي زيارات طبية الشهر اللي فات
        "clinics_no_visits": """
            SELECT c.ClinicID, c.Location FROM CLINIC c
            LEFT JOIN MedicalVisit mv ON c.ClinicID = mv.ClinicID
              AND MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            WHERE mv.VisitID IS NULL;
        """,
        # 3. أكتر دكتور إدى تطعيمات الشهر اللي فات
        "top_vaccinating_vet": """
            SELECT TOP 1 mv.VetID, COUNT(vr.VaccinationID) AS TotalVaccinations
            FROM MedicalVisit mv JOIN VaccinationRecord vr ON mv.VisitID = vr.VisitID
            WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            GROUP BY mv.VetID ORDER BY TotalVaccinations DESC;
        """,
        # 4. أصحاب الحيوانات اللي مجابوش حيواناتهم العيادة الشهر اللي فات
        "owners_no_visits": """
            SELECT o.OwnerID, o.BillingAddress FROM Owner o
            WHERE o.OwnerID NOT IN (
                SELECT mv.OwnerID FROM MedicalVisit mv
                WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
                  AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            );
        """,
        # 5. أنواع التطعيمات المحددة اللي اتعطت في كل عيادة الشهر اللي فات
        "vaccines_per_clinic": """
            SELECT c.Location, vr.VaccineType FROM CLINIC c
            JOIN MedicalVisit mv ON c.ClinicID = mv.ClinicID
            JOIN VaccinationRecord vr ON mv.VisitID = vr.VisitID
            WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            GROUP BY c.Location, vr.VaccineType;
        """,
        # 6. لكل حيوان، اسمه وإجمالي عدد زياراته خلال السنة الحالية
        "pet_visits_this_year": """
            SELECT p.Name, COUNT(mv.VisitID) AS TotalVisits FROM Pet p
            LEFT JOIN MedicalVisit mv ON p.PetID = mv.PetID AND YEAR(mv.Date) = YEAR(GETDATE())
            GROUP BY p.Name;
        """
    }
