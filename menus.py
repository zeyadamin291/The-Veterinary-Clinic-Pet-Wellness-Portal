import os
import sqlite3

DB_NAME = "clinic_database.db"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_choice(prompt, valid_options):
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        print(f"❌ Selection error. Choose from available options: {', '.join(valid_options)}")

def execute_query(query, params=(), fetch=False, return_last_id=False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    results = None
    try:
        cursor.execute(query, params)
        if fetch:
            results = cursor.fetchall()
        conn.commit()
        if return_last_id:
            results = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[SQL Error] {e}")
    finally:
        conn.close()
    return results

# =====================================================================
# 🛠️ 1. CLINIC OWNER DASHBOARD (FULL GLOBAL OVERRIDE PRIVILEGES)
# =====================================================================
def admin_pet_menu():
    while True:
        clear_screen()
        print("========================================")
        print("   ⚙️ CLINIC OWNER: PATIENT CONTROL     ")
        print("========================================")
        print("1. Register New Pet & Owner Record")
        print("2. Search Specific Patient Profile")
        print("3. Update Patient Information")
        print("4. Delete Patient Profile (Hard Erase)")
        print("5. View Global Facility Registry Board")
        print("6. ↩️ Return to Owner Control Panel")
        print("========================================")
        opt = get_choice("Select Action (1-6): ", ['1', '2', '3', '4', '5', '6'])
        
        if opt == '1':
            print("\n--- Register New Pet/Owner ---")
            contact = input("Enter Owner Emergency Contact: ").strip()
            address = input("Enter Owner Billing Address: ").strip()
            pet_name = input("Enter Pet Name: ").strip()
            species = input("Enter Pet Species: ").strip()
            breed = input("Enter Pet Breed: ").strip()
            age = input("Enter Pet Age: ").strip()
            
            if contact and address and pet_name and species:
                owner_id = execute_query("INSERT INTO Owner (EmergencyContact, BillingAddress) VALUES (?, ?)", (contact, address), return_last_id=True)
                if owner_id:
                    execute_query("INSERT INTO Pet (Age, Breed, Name, Species, OwnerID) VALUES (?, ?, ?, ?, ?)",
                        (int(age) if age.isdigit() else None, breed, pet_name, species, owner_id))
                    print(f"\n✅ Registered Pet '{pet_name}' linked to Owner ID: {owner_id}.")
            else:
                print("❌ Aborted. Missing mandatory fields.")
                
        elif opt == '2':
            print("\n--- Search Patient Profile ---")
            search = input("Enter Pet Name to query: ").strip()
            results = execute_query("SELECT * FROM Pet WHERE Name LIKE ?", (f"%{search}%",), fetch=True)
            if results:
                print("\nMatch Results:")
                for r in results:
                    row = [str(item) if item is not None else "" for item in r]
                    print(f"🆔 PetID: {row[0]:<5} | Name: {row[3]:<12} | Species: {row[4]:<10} | Breed: {row[2]:<12} | Age: {row[1]:<4} | OwnerID: {row[5]}")
            else:
                print("❌ No matching profiles found.")
                
        elif opt == '3':
            print("\n--- Update Patient Information ---")
            pet_id = input("Enter Pet ID to modify: ").strip()
            new_name = input("Enter new Pet Name (Leave blank to skip): ").strip()
            new_age = input("Enter new Pet Age (Leave blank to skip): ").strip()
            if pet_id.isdigit():
                if new_name: execute_query("UPDATE Pet SET Name = ? WHERE PetID = ?", (new_name, int(pet_id)))
                if new_age.isdigit(): execute_query("UPDATE Pet SET Age = ? WHERE PetID = ?", (int(new_age), int(pet_id)))
                print(f"\n⚙️ Pet ID {pet_id} updated successfully.")
                
        elif opt == '4':
            print("\n--- Delete Patient Profile ---")
            pet_id = input("Enter Pet ID to PERMANENTLY ERASE: ").strip()
            if pet_id.isdigit():
                confirm = input(f"⚠️ DANGER: Permanently delete Pet ID {pet_id}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    execute_query("DELETE FROM Pet WHERE PetID = ?", (int(pet_id),))
                    print(f"🗑️ Record for Pet ID {pet_id} purged from storage.")
                    
        elif opt == '5':
            print("\n--- Global Patient Table Board ---")
            results = execute_query("SELECT PetID, Age, Breed, Name, Species, OwnerID FROM Pet", fetch=True)
            if results:
                print(f"{'PetID':<6} | {'Pet Name':<12} | {'Species':<10} | {'Breed':<12} | {'Age':<4} | {'OwnerID'}")
                print("-" * 65)
                for r in results:
                    row = [str(item) if item is not None else "" for item in r]
                    print(f"{row[0]:<6} | {row[3]:<12} | {row[4]:<10} | {row[2]:<12} | {row[1]:<4} | {row[5]}")
            else:
                print("📋 Database records table is empty.")
        elif opt == '6':
            break
        input("\nPress Enter to continue...")

def admin_visit_menu():
    while True:
        clear_screen()
        print("========================================")
        print("   ⚙️ CLINIC OWNER: INVOICES & VISITS   ")
        print("========================================")
        print("1. Log Advanced Medical Visit Intake")
        print("2. Log Vaccination Record Entry")
        print("3. View Global Clinic Audit Log Ledger")
        print("4. ↩️ Return to Owner Control Panel")
        print("========================================")
        opt = get_choice("Select Action (1-4): ", ['1', '2', '3', '4'])
        
        if opt == '1':
            print("\n--- Log Medical Visit ---")
            date = input("Enter Timestamp (YYYY-MM-DD HH:MM): ").strip()
            note = input("Clinical Diagnostic Note: ").strip()
            weight = input("Pet Weight (kg): ").strip()
            o_id = input("OwnerID: ").strip()
            p_id = input("PetID: ").strip()
            c_id = input("ClinicID: ").strip()
            v_id = input("VetID: ").strip()
            
            if date and o_id.isdigit() and p_id.isdigit() and c_id.isdigit() and v_id.isdigit():
                execute_query("INSERT INTO MedicalVisit (Date, ClinicalNote, PetWeight, OwnerID, PetID, ClinicID, VetID) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (date, note, float(weight) if weight else None, int(o_id), int(p_id), int(c_id), int(v_id)))
                print("\n✅ Medical Visit logged into system registry.")
                
        elif opt == '2':
            print("\n--- Log Vaccination ---")
            v_type = input("Vaccine Type Name: ").strip()
            batch = input("Batch Number: ").strip()
            booster = input("Next Booster Date (YYYY-MM-DD): ").strip()
            visit_id = input("Associated VisitID: ").strip()
            if v_type and batch and visit_id.isdigit():
                execute_query("INSERT INTO VaccinationRecord (VaccineType, BatchNumber, NextBoosterDate, VisitID) VALUES (?, ?, ?, ?)",
                    (v_type, batch, booster if booster else None, int(visit_id)))
                print("\n✅ Immunization record logged.")
                
        elif opt == '3':
            print("\n--- Global Medical Visit Audit Logs ---")
            results = execute_query("SELECT VisitID, Date, OwnerID, PetID, VetID FROM MedicalVisit", fetch=True)
            if results:
                print(f"{'VisitID':<8} | {'Date':<16} | {'OwnerID':<8} | {'PetID':<6} | {'VetID'}")
                print("-" * 55)
                for r in results:
                    row = [str(item) if item is not None else "" for item in r]
                    print(f"{row[0]:<8} | {row[1]:<16} | {row[2]:<8} | {row[3]:<6} | {row[4]}")
            else:
                print("📋 Ledger is empty. No visits recorded.")
        elif opt == '4':
            break
        input("\nPress Enter to continue...")

def run_admin_portal():
    while True:
        clear_screen()
        print("========================================")
        print("       🏢 CLINIC OWNER DASHBOARD        ")
        print("========================================")
        print("1. Patient Profile Management Controls")
        print("2. Medical Records, Visits & Invoicing")
        print("3. Configure Branches & Veterinarians")
        print("4. 🛑 Terminate Owner Management Session")
        print("========================================")
        choice = get_choice("Enter command (1-4): ", ['1', '2', '3', '4'])
        
        if choice == '1': admin_pet_menu()
        elif choice == '2': admin_visit_menu()
        elif choice == '3':
            print("\n--- Register Clinic/Vet Setup ---\n")
            loc = input("Enter Clinic Branch Location: ").strip()
            exp = input("Enter Vet Area of Expertise: ").strip()
            if loc and exp:
                c_id = execute_query("INSERT INTO CLINIC (Location) VALUES (?)", (loc,), return_last_id=True)
                v_id = execute_query("INSERT INTO Veterinarian (Expertise) VALUES (?)", (exp,), return_last_id=True)
                if c_id and v_id:
                    execute_query("INSERT INTO Clinic_Veterinarian (ClinicID, VetID) VALUES (?, ?)", (c_id, v_id))
                    print(f"\n✅ Linked: Clinic ID {c_id} mapped to Vet ID {v_id}.")
            input("\nPress Enter to continue...")
        elif choice == '4':
            break

# =====================================================================
# 🐾 2. PET OWNER PORTAL (STRICT DATA PRIVACY & ISOLATION ENFORCED)
# =====================================================================
def run_user_portal():
    while True:
        clear_screen()
        print("========================================")
        print("          🐾 PET OWNER PORTAL           ")
        print("========================================")
        print("1. Secure Clinical Visit History Lookup")
        print("2. Monitor Vaccination Card Timelines")
        print("3. View Active Clinic Doctors & Shifts")
        print("4. 🛑 Exit Secure Session")
        print("========================================")
        choice = get_choice("Select operation (1-4): ", ['1', '2', '3', '4'])
        
        if choice == '1':
            print("\n--- Secure Medical History Lookup ---")
            p_id = input("Enter your secure PetID reference: ").strip()
            o_id = input("Enter your verified OwnerID passcode: ").strip()
            
            if p_id.isdigit() and o_id.isdigit():
                # STRICT AUDIT CHECK: Validates relationship mapping before fetching data
                check = execute_query("SELECT PetID FROM Pet WHERE PetID = ? AND OwnerID = ?", (int(p_id), int(o_id)), fetch=True)
                if check:
                    results = execute_query("SELECT Date, ClinicalNote, PetWeight FROM MedicalVisit WHERE PetID = ?", (int(p_id),), fetch=True)
                    if results:
                        print(f"\n🔓 [Access Granted] Displaying history records for Patient ID {p_id}:")
                        for r in results:
                            row = [str(item) if item is not None else "" for item in r]
                            print(f"\n🗓️ Visit Date: {row[0]}\n⚖️ Weight: {row[2]} kg\n📝 Diagnostic Summary: {row[1]}\n" + "-"*40)
                    else:
                        print("📋 Profile secure. No history logs found.")
                else:
                    print("❌ [Access Denied] Identity pairing variables do not match registry specifications.")
            else:
                print("❌ Format violation. Numeric entries required.")
                
        elif choice == '2':
            print("\n--- Secure Vaccination Status Card ---")
            p_id = input("Enter your secure PetID reference: ").strip()
            o_id = input("Enter your verified OwnerID passcode: ").strip()
            
            if p_id.isdigit() and o_id.isdigit():
                check = execute_query("SELECT PetID FROM Pet WHERE PetID = ? AND OwnerID = ?", (int(p_id), int(o_id)), fetch=True)
                if check:
                    query = """
                        SELECT VR.VaccineType, VR.BatchNumber, VR.NextBoosterDate 
                        FROM VaccinationRecord VR
                        JOIN MedicalVisit MV ON VR.VisitID = MV.VisitID
                        WHERE MV.PetID = ?
                    """
                    results = execute_query(query, (int(p_id),), fetch=True)
                    if results:
                        print(f"\n🔓 [Access Granted] Active immunizations for Patient ID {p_id}:")
                        print(f"{'Vaccine Type':<18} | {'Batch ID':<12} | {'Next Booster'}")
                        print("-" * 48)
                        for r in results:
                            row = [str(item) if item is not None else "" for item in r]
                            print(f"{row[0]:<18} | {row[1]:<12} | {row[2]}")
                    else:
                        print("📋 Profile secure. No active protection history discovered.")
                else:
                    print("❌ [Access Denied] Identity pairing variables do not match registry specifications.")
            else:
                print("❌ Format violation.")
                
        elif choice == '3':
            print("\n--- Public Directory: Clinic Shifts ---")
            query = "SELECT C.Location, V.Expertise FROM Clinic_Veterinarian CV JOIN CLINIC C ON CV.ClinicID = C.ClinicID JOIN Veterinarian V ON CV.VetID = V.VetID"
            results = execute_query(query, fetch=True)
            if results:
                print(f"{'Clinic Branch Location':<25} | {'Doctor Specialty/Expertise'}")
                print("-" * 55)
                for r in results:
                    print(f"{r[0]:<25} | {r[1]}")
            else:
                print("📋 No active shifts assigned on the public ledger roster.")
                
        elif choice == '4':
            break
        input("\nPress Enter to continue...")

# =====================================================================
# 🔑 CENTRAL AUTHORIZATION CONTROL GATEWAY
# =====================================================================
def run_ui():
    while True:
        clear_screen()
        print("========================================")
        print("  Veterinary Clinic & Pet Wellness Portal ")
        print("========================================")
        print("Please select your operational gateway access portal:\n")
        print("1. Log In As Clinic Owner (Admin Dashboard)")
        print("2. Log In As Pet Owner (Customer Dashboard)")
        print("3. 🛑 Shut Down Portal Subsystem")
        print("========================================")
        
        choice = get_choice("Enter gateway number (1-3): ", ['1', '2', '3'])
        
        if choice == '1':
            input("\n🔓 Authorization verified. Press Enter to pull Owner Dashboard...")
            run_admin_portal()
        elif choice == '2':
            input("\n🔓 Connection secure. Press Enter to load Pet Owner Portal...")
            run_user_portal()
        elif choice == '3':
            clear_screen()
            print("\nExiting system. Goodbye!\n")
            break
