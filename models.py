class Owner:
    def __init__(self, owner_id, name, billing_address, emergency_contact):
        self.owner_id          = owner_id
        self.name              = name
        self.billing_address   = billing_address
        self.emergency_contact = emergency_contact

    def __str__(self):
        return f"Owner [{self.owner_id}]: {self.name} | Contact: {self.emergency_contact}"


class Pet:
    def __init__(self, pet_id, owner_id, name, species, breed, age):
        self.pet_id   = pet_id
        self.owner_id = owner_id
        self.name     = name
        self.species  = species
        self.breed    = breed
        self.age      = age

    def __str__(self):
        return f"Pet [{self.pet_id}]: {self.name} | {self.species} | Age: {self.age}"


class Clinic:
    def __init__(self, clinic_id, name, location, emergency_facilities):
        self.clinic_id            = clinic_id
        self.name                 = name
        self.location             = location
        self.emergency_facilities = emergency_facilities

    def __str__(self):
        return f"Clinic [{self.clinic_id}]: {self.name} | {self.location}"


class Veterinarian:
    def __init__(self, vet_id, name, email, phone):
        self.vet_id = vet_id
        self.name   = name
        self.email  = email
        self.phone  = phone

    def __str__(self):
        return f"Vet [{self.vet_id}]: {self.name} | {self.email}"


class VetSpecialty:
    def __init__(self, specialty_id, vet_id, specialty_name):
        self.specialty_id   = specialty_id
        self.vet_id         = vet_id
        self.specialty_name = specialty_name

    def __str__(self):
        return f"Specialty [{self.specialty_id}]: {self.specialty_name}"


class Visit:
    def __init__(self, visit_id, pet_id, vet_id, clinic_id, visit_date):
        self.visit_id   = visit_id
        self.pet_id     = pet_id
        self.vet_id     = vet_id
        self.clinic_id  = clinic_id
        self.visit_date = visit_date

    def __str__(self):
        return f"Visit [{self.visit_id}]: Date: {self.visit_date} | Pet: {self.pet_id} | Vet: {self.vet_id}"


class ClinicalNote:
    def __init__(self, note_id, visit_id, weight, diagnosis, notes):
        self.note_id   = note_id
        self.visit_id  = visit_id
        self.weight    = weight
        self.diagnosis = diagnosis
        self.notes     = notes

    def __str__(self):
        return f"Note [{self.note_id}]: Weight: {self.weight}kg | Diagnosis: {self.diagnosis}"


class Vaccination:
    def __init__(self, vaccine_id, note_id, vaccine_type, batch_number,
                 date_administered, booster_due_date):
        self.vaccine_id        = vaccine_id
        self.note_id           = note_id
        self.vaccine_type      = vaccine_type
        self.batch_number      = batch_number
        self.date_administered = date_administered
        self.booster_due_date  = booster_due_date

    def __str__(self):
        return f"Vaccine [{self.vaccine_id}]: {self.vaccine_type} | Booster: {self.booster_due_date}"


class Reminder:
    def __init__(self, reminder_id, vaccine_id, owner_id,
                 reminder_date, status='pending'):
        self.reminder_id   = reminder_id
        self.vaccine_id    = vaccine_id
        self.owner_id      = owner_id
        self.reminder_date = reminder_date
        self.status        = status

    def __str__(self):
        return f"Reminder [{self.reminder_id}]: {self.reminder_date} | Status: {self.status}"


class VaccineInventory:
    def __init__(self, inventory_id, clinic_id, vaccine_type, stock_level):
        self.inventory_id = inventory_id
        self.clinic_id    = clinic_id
        self.vaccine_type = vaccine_type
        self.stock_level  = stock_level

    def __str__(self):
        return f"Inventory [{self.inventory_id}]: {self.vaccine_type} | Stock: {self.stock_level}"