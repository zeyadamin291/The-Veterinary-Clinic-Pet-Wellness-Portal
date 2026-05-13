
def get_queries():
    return {
        # 1. أكتر فصيلة (Species) عملت زيارات طبية الشهر اللي فات
        "max_species_visits": """
            SELECT TOP 1 p.Species, COUNT(mv.VisitID) AS TotalVisits
            FROM Pet p
            JOIN MedicalVisit mv ON p.PetID = mv.PetID
            WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            GROUP BY p.Species
            ORDER BY TotalVisits DESC;
        """,

        # 2. العيادة اللي معملتش أي زيارات طبية الشهر اللي فات
        "clinics_no_visits": """
            SELECT c.ClinicID, c.Location
            FROM CLINIC c
            LEFT JOIN MedicalVisit mv ON c.ClinicID = mv.ClinicID 
              AND MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            WHERE mv.VisitID IS NULL;
        """,

        # 3. أكتر دكتور إدى تطعيمات الشهر اللي فات
        "top_vaccinating_vet": """
            SELECT TOP 1 mv.VetID, COUNT(vr.VaccinationID) AS TotalVaccinations
            FROM MedicalVisit mv
            JOIN VaccinationRecord vr ON mv.VisitID = vr.VisitID
            WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            GROUP BY mv.VetID
            ORDER BY TotalVaccinations DESC;
        """,

        # 4. أصحاب الحيوانات اللي مجابوش حيواناتهم العيادة الشهر اللي فات
        "owners_no_visits": """
            SELECT o.OwnerID, o.BillingAddress
            FROM Owner o
            WHERE o.OwnerID NOT IN (
                SELECT mv.OwnerID
                FROM MedicalVisit mv
                WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
                  AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            );
        """,

        # 5. أنواع التطعيمات المحددة اللي اتعطت في كل عيادة الشهر اللي فات
        "vaccines_per_clinic": """
            SELECT c.Location, vr.VaccineType
            FROM CLINIC c
            JOIN MedicalVisit mv ON c.ClinicID = mv.ClinicID
            JOIN VaccinationRecord vr ON mv.VisitID = vr.VisitID
            WHERE MONTH(mv.Date) = MONTH(DATEADD(month, -1, GETDATE()))
              AND YEAR(mv.Date) = YEAR(DATEADD(month, -1, GETDATE()))
            GROUP BY c.Location, vr.VaccineType;
        """,

        # 6. لكل حيوان، اسمه وإجمالي عدد زياراته خلال السنة الحالية
        "pet_visits_this_year": """
            SELECT p.Name, COUNT(mv.VisitID) AS TotalVisits
            FROM Pet p
            LEFT JOIN MedicalVisit mv ON p.PetID = mv.PetID 
              AND YEAR(mv.Date) = YEAR(GETDATE())
            GROUP BY p.Name;
        """
    }
