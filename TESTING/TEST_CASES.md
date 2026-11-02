# CCMS Software Test Specifications & Execution Report
## Classified Testing Suite: Black Box, White Box & Selenium 4

---

### Executive Test Summary

| Testing Category | Sub-Division | Test Modules | Total Cases | Passed | Pass Rate |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Black Box Testing** | `TESTING/black_box/` | Positive, Negative, Boundary, Functional | 22 | 22 | **100%** |
| **White Box Testing** | `TESTING/white_box/` | Database Integrity, Calculation Logic, Role Matrix | 9 | 9 | **100%** |
| **Selenium 4 Testing**| `TESTING/selenium/`  | Headless Chrome UI, E2E Theme, Catalog, Auth | 9 | 9 | **100%** |
| **Total** | | | **40** | **40** | **100%** |

---

## 1. Black Box Testing Suite (`TESTING/black_box/`)
Specification-based and behavioral testing focusing on external inputs, system responses, user journeys, boundary analysis, and error recovery.

### 1.1 Positive Scenarios (`test_positive_scenarios.py`)
- **TC-BB-POS-01**: Landing page accessibility and brand title verification (HTTP 200).
- **TC-BB-POS-02**: Clubs catalog route availability (`/clubs`).
- **TC-BB-POS-03**: Authentication login route availability (`/login`).
- **TC-BB-POS-04**: User registration route availability (`/register`).
- **TC-BB-POS-05**: Supabase club categories retrieval (HTTP 200).
- **TC-BB-POS-06**: Active clubs catalog retrieval (HTTP 200, status `'approved'`).
- **TC-BB-POS-07**: Modern ES module static asset delivery.

### 1.2 Negative Scenarios (`test_negative_scenarios.py`)
- **TC-BB-NEG-01**: Rejection of invalid passwords during login (HTTP 400).
- **TC-BB-NEG-02**: Non-existent user credential rejection without system disclosure (HTTP 400/422).
- **TC-BB-NEG-03**: Prevention of unauthorized profile role privilege elevation.
- **TC-BB-NEG-04**: Prevention of anonymous direct writes to attendance table.
- **TC-BB-NEG-05**: Graceful empty response handling on non-existent club slug lookup.

### 1.3 Boundary Value Analysis (`test_boundary_scenarios.py`)
- **TC-BB-BND-01**: Event capacity boundary at 0 (unregistrable event).
- **TC-BB-BND-02**: Capacity ceiling boundary validation (`current_count >= max_capacity`).
- **TC-BB-BND-03**: Empty string search boundary returning full catalog without crashes.
- **TC-BB-BND-04**: Extreme length search string boundary (2,500 characters) buffer overflow safety.
- **TC-BB-BND-05**: Malformed UUID string boundary producing standard validation errors (HTTP 400).

### 1.4 Functional Workflows (`test_functional_workflows.py`)
- **TC-BB-FNC-01**: Membership lifecycle state machine validation (`pending`, `approved`, `rejected`, `inactive`).
- **TC-BB-FNC-02**: Attendance status domain constraint verification (`present`, `absent`, `late`).
- **TC-BB-FNC-03**: SPA client-side fallback routing (`index.html` delivery for deep links).
- **TC-BB-FNC-04**: Empty JSON payload rejection at authentication endpoints.
- **TC-BB-FNC-05**: Resilient error recovery when supplied with malformed raw non-JSON payloads.

---

## 2. White Box Testing Suite (`TESTING/white_box/`)
Structural, logic-driven, and code-level verification inspecting internal data structures, branch coverage, database constraints, and permission matrices.

### 2.1 Database Integrity & Contracts (`test_database_integrity.py`)
- **TC-WB-DB-01**: Foreign key constraint cascade enforcement blocking orphaned category assignments.
- **TC-WB-DB-02**: PostgREST server-side CORS preflight header contract validation.
- **TC-WB-DB-03**: Supabase GoTrue Auth service internal health status verification.
- **TC-WB-DB-04**: Bidirectional network connectivity between presentation tier and data tier.

### 2.2 Internal Calculation & Algorithmic Logic (`test_calculation_logic.py`)
- **TC-WB-CALC-01**: Complete branch coverage of attendance percentage calculation logic:
  - Branch 1: Zero-division guard for empty records list $\rightarrow$ `0.0%`.
  - Branch 2: 100% attendance calculation (`present` and `late` sessions).
  - Branch 3: Fractional decimal rounding (e.g., 2/3 $\rightarrow$ `66.7%`).
  - Branch 4: 0% attendance calculation (`absent` sessions).
- **TC-WB-CALC-02**: Internal array grouping and filtering algorithm by student academic department.
- **TC-WB-CALC-03**: Password length boundary evaluation logic enforcing minimum 6-character constraints.

### 2.3 Role Hierarchy & Taxonomy Integrity (`test_role_hierarchy_permissions.py`)
- **TC-WB-ROLE-01**: Strict dual-role permission matrix validation:
  - Student role: browse, apply, view timetable, view attendance.
  - Faculty coordinator role: approve members, publish timetables, record roll calls.
  - Deprecated admin role prevention.
- **TC-WB-ROLE-02**: Internal relational taxonomy integrity ensuring no orphaned club records exist.

---

## 3. Selenium 4 End-to-End Browser Testing Suite (`TESTING/selenium/`)
Automated browser-driven validation using **Selenium 4 WebDriver** with Headless Google Chrome.

### 3.1 Landing Page & Theme Switcher (`test_landing_page_ui.py`)
- **TC-SEL-01**: Headless browser page load, title verification ("CCMS — College Club Management System"), and brand heading rendering.
- **TC-SEL-02**: Interactive theme switcher button interaction (toggling between Dark Mode and Light Mode with DOM attribute verification).
- **TC-SEL-03**: Top navigation bar elements presence (Portals, Activity Timetable, Features, Directory).

### 3.2 Clubs Catalog & Interactive Filters (`test_clubs_catalog_ui.py`)
- **TC-SEL-04**: Navigation to `/clubs` route and verification of club cards rendering.
- **TC-SEL-05**: Interactive domain category filter buttons and search input display.

### 3.3 Authentication Forms & Role Selection (`test_auth_forms_ui.py`)
- **TC-SEL-06**: Login form input element visibility (email, password, submit button).
- **TC-SEL-07**: Registration form role selector tabs (Student vs Coordinator) and field rendering.

### 3.4 Activity Timetable & Dual Portals (`test_timetable_display_ui.py`)
- **TC-SEL-08**: Activity timetable section display and session day cards (Monday, Wednesday, Saturday) with venue rooms and timings.
- **TC-SEL-09**: Dual portal card elements for Student Portal and Faculty Coordinator Hub.

---

## 4. Test Execution Instructions

### Running the Entire Classified Test Suite
```bash
python -m pytest TESTING/ -v
```

### Running Specific Subdivisions
```bash
# 1. Run only Black Box tests
python -m pytest TESTING/black_box/ -v

# 2. Run only White Box tests
python -m pytest TESTING/white_box/ -v

# 3. Run only Selenium 4 browser tests
python -m pytest TESTING/selenium/ -v
```
