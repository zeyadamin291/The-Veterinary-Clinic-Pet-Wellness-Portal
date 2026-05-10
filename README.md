# Project Structure

The project follows a simple modular structure to keep the code organized and easy to maintain.

```text
vet-clinic/
│
├── main.py
├── database.py
├── models.py
├── services.py
├── menus.py
├── queries.py
├── utils.py
├── schema.sql
└── README.md
```

---

## File Descriptions

### `main.py`

The entry point of the application.
Starts the console application and displays the main menu.

---

### `database.py`

Handles the connection to SQL Server and executes SQL queries.

Responsibilities:

* Connecting to the database
* Executing queries
* Committing changes
* Fetching data

---

### `models.py`

Contains the main system classes (entities).

Examples:

* Owner
* Pet
* Clinic
* Veterinarian
* Visit
* Vaccination

---

### `services.py`

Contains the business logic of the system.

Examples:

* Adding pets
* Scheduling visits
* Registering vaccinations
* Managing owners and clinics

---

### `menus.py`

Handles all console menus and user interaction.

Responsibilities:

* Displaying menu options
* Reading user input
* Navigating between features

---

### `queries.py`

Contains the required inquiry/report SQL queries.

Examples:

* Most visited pet species
* Veterinarian with highest vaccinations
* Clinics without visits
* Pet visit statistics

---

### `utils.py`

Contains helper functions used across the project.

Examples:

* Input validation
* Formatting outputs
* Utility methods


---

### `schema.sql`

Contains the SQL database schema.

Responsibilities:

* Creating the database
* Creating tables
* Defining relationships and constraints

---

### `README.md`

Contains project documentation and setup instructions.
