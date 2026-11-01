# CCMS — College Club Management System
## Official User Manual & Operational Guide

---

### Table of Contents
1. [Overview & Architecture](#1-overview--architecture)
2. [Dual-Role System](#2-dual-role-system)
   - [Student Role](#student-role)
   - [Faculty Coordinator Role](#faculty-coordinator-role)
3. [Visual Theme & Accessibility](#3-visual-theme--accessibility)
4. [Step-by-Step User Workflows](#4-step-by-step-user-workflows)
   - [Student: Club Exploration & Application](#workflow-a-student-club-exploration--application)
   - [Faculty: Department Sorting & Colorful Email Approval](#workflow-b-faculty-department-sorting--approval)
   - [Activity Timetable Management](#workflow-c-activity-timetable-management)
   - [Session Attendance Tracking](#workflow-d-session-attendance-tracking)
5. [Automated Test Suite (Pytest)](#5-automated-test-suite-pytest)
6. [Local Setup & Deployment Guide](#6-local-setup--deployment-guide)
7. [Vercel Hosting Configuration](#7-vercel-hosting-configuration)

---

### 1. Overview & Architecture

The **College Club Management System (CCMS)** is an institutional extracurricular platform designed to connect undergraduate and postgraduate students with departmental faculty mentors. 

CCMS streamlines campus club operations by replacing fragmented social media groups, paper slips, and notice boards with a verified, accessible digital workspace:
- **Direct Mentorship**: Eliminates administrative bottlenecks by focusing strictly on direct peer-to-mentor interaction between **Students** and **Faculty Coordinators**.
- **Institutional Accreditation**: Digital session attendance check-ins create verifiable co-curricular records.
- **Departmental Harmony**: Student applicants are sorted by collegiate department for balanced team formation.
- **Instant Communication**: Welcome acceptance emails are dispatched with branded, colorful templates.

---

### 2. Dual-Role System

CCMS operates under a streamlined **two-role access control model**:

```
+-------------------------------------------------------------+
|                  COLLEGE CLUB PLATFORM                      |
+------------------------------+------------------------------+
|         STUDENT ROLE         |   FACULTY COORDINATOR ROLE   |
+------------------------------+------------------------------+
| • Browse Club Directories   | • Department-Wise Sorting    |
| • Send Joining Applications  | • 1-Click Acceptance Emails  |
| • Sync Weekly Timetables     | • Publish Activity Timetable |
| • Track Session Attendance   | • Mark Digital Attendance    |
| • Verified Transcript Log    | • Monitor Cohort Analytics   |
+------------------------------+------------------------------+
```

#### Student Role
- **Exploration**: Access the `/clubs` catalog filtered by domain (Tech & AI, Robotics & IoT, Design & Media, Cultural Arts, Athletics & Esports).
- **Joining Applications**: Submit digital applications with department information and a motivation statement directly to the faculty lead.
- **Activity Timetable**: Check weekly club schedules, meeting rooms, workshop syllabi, and seat capacities.
- **Attendance Portfolio**: View verified session attendance logs with real-time percentage tracking for academic credit claims.

#### Faculty Coordinator Role
- **Department Sorting**: Filter and organize applicants by academic department (e.g., Computer Science, Electronics & Communication, Mechanical Engineering, Visual Arts) to ensure diverse cohort representation.
- **Colorful Email Approvals**: Approve applications with a single click, instantly dispatching a colorful, officially formatted welcome email to the student inbox.
- **Timetable Scheduling**: Create, update, and publish weekly lab sessions, hackathons, and guest seminars.
- **Digital Roll Call**: Mark student check-ins (Present, Absent, Late) during club gatherings.

---

### 3. Visual Theme & Accessibility

CCMS incorporates an institutional **Dark & Light Mode** system:
- **Theme Switcher**: Located in the top navigation bar with a single-click Sun / Moon icon.
- **Color Contrast**: All typography adheres to WCAG AA high-contrast standards, ensuring text remains sharp and readable in both modes.
- **Clean Iconography**: Uses clean, professional SVG icons (`lucide-react`) rather than distracting decorative emojis.

---

### 4. Step-by-Step User Workflows

#### Workflow A: Student Club Exploration & Application
1. **Visit Landing Page**: Navigate to the homepage to view active campus clubs and quick timetable highlights.
2. **Registration / Login**: 
   - Click **Get Started** (`/register`) to create a student account.
   - Enter your name, student email, and password.
3. **Explore Clubs**:
   - Go to **Clubs Directory** (`/clubs`).
   - Use the category tabs or search bar to discover clubs matching your domain interests.
4. **Submit Application**:
   - Open a club card to view its description, faculty coordinator details, and timetable.
   - Click **Send Joining Application** and specify your college department.
   - Confirmation is delivered instantly to your student portal.

#### Workflow B: Faculty Department Sorting & Approval
1. **Faculty Access**: Sign in via `/login` using faculty coordinator credentials.
2. **Review Applicants**:
   - Navigate to the **Faculty Coordinator Hub** (`/coordinator/dashboard`).
   - Under **Membership Registrations**, view all pending student applications.
3. **Sort by Department**:
   - Use the department filter dropdown to view applicants grouped by **CSE**, **ECE**, **MECH**, or **ARTS**.
4. **Approve Candidate**:
   - Click **Approve Member**.
   - CCMS updates the membership state and dispatches a colorful, official welcome acceptance email directly to the student's email address.

#### Workflow C: Activity Timetable Management
1. In the Coordinator Hub, select **Manage Timetable**.
2. Define the session title, day of the week, starting and ending time, venue/lab room number, and participant capacity.
3. Click **Publish to Timetable**. The slot immediately appears in the student's calendar feed and the public timetable showcase.

#### Workflow D: Session Attendance Tracking
1. At the beginning of a club gathering, the coordinator opens **Session Attendance**.
2. The roster displays enrolled students sorted by department.
3. Mark attendance status for each member (`Present`, `Absent`, or `Late`).
4. Click **Submit Attendance**. Real-time attendance percentages are recalculated for student academic transcripts.

---

### 5. Automated Test Suite (Pytest)

The system includes a 30-case automated test suite in the `TESTING/` directory:

| Test Module | Coverage | Status |
| :--- | :--- | :--- |
| `test_positive.py` | Route availability, static asset delivery, database reads | **PASS** |
| `test_negative.py` | Invalid passwords, non-existent users, privilege escalation blocks | **PASS** |
| `test_boundary.py` | Zero capacity limits, boundary search strings, malformed UUIDs | **PASS** |
| `test_functional.py` | Taxonomy integrity, attendance math, membership lifecycles | **PASS** |
| `test_integration.py`| Supabase REST headers, foreign key cascades, auth health | **PASS** |
| `test_validation_error_handling.py` | Payload rejection, password constraints, SPA fallback | **PASS** |

To execute the test suite:
```bash
python -m pytest TESTING/ -v
```

---

### 6. Local Setup & Deployment Guide

#### Prerequisites
- Node.js 18+ (tested with Node 20 / 22 / 25)
- Python 3.10+ (for automated test suite)
- Git

#### Installation Steps
```bash
# 1. Clone repository
git clone https://github.com/NAVXXN0611/Club-Management-System-.git
cd Club-Management-System-

# 2. Install dependencies
npm install

# 3. Configure environment variables
# Copy .env.example to .env.local and update with your Supabase keys
cp .env.example .env.local

# 4. Start local development server
npm run dev

# 5. Build for production
npm run build
```

---

### 7. Vercel Hosting Configuration

The project is preconfigured for single-page application (SPA) hosting on Vercel via [`vercel.json`](file:///e:/Club%20Management%20System/vercel.json):

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

#### Deploying to Vercel via CLI
```bash
vercel --prod
```
The client build is automatically bundled by Vite and deployed across global edge networks with instant cache invalidation.
