# College Club Management System

## Antigravity Build Guide --- React + TypeScript + Supabase + Vercel + GitHub

> **Project vision:** One platform. Every club. Every student. Every
> activity.

------------------------------------------------------------------------

## 0. What this project is

The **College Club Management System (CCMS)** is a web application that
centralizes academic and non-academic college clubs into one digital
platform.

### Current problem

Students often discover clubs through different channels:

-   Google Forms sent through email
-   QR codes linked to Google Forms
-   WhatsApp messages/groups
-   Posters and notices
-   Separate registration links
-   Separate attendance sheets
-   Separate club announcements

After joining, students may still have difficulty finding:

-   Their club memberships
-   Upcoming activities
-   Event registration
-   Attendance
-   Announcements
-   Participation history
-   Certificates or achievements

### Proposed solution

CCMS provides one place where students can:

1.  Discover all college clubs.
2.  Filter academic/non-academic clubs.
3.  View club profiles.
4.  Apply for club membership.
5.  Register for club events.
6.  Receive announcements.
7.  View attendance.
8.  Track participation.
9.  Build a club activity profile.

Club coordinators can:

1.  Manage club information.
2.  Review membership applications.
3.  Create events.
4.  Manage event registrations.
5.  Mark attendance.
6.  Publish announcements.
7.  View club analytics.
8.  Generate reports.

College administrators can:

1.  Approve/manage clubs.
2.  Manage users and coordinators.
3.  Monitor overall club activity.
4.  View college-level analytics.
5.  Manage categories and system settings.

------------------------------------------------------------------------

# 1. Project pitch

### One-line pitch

> **CCMS is a centralized digital platform that replaces scattered club
> registration forms, QR codes, spreadsheets, and announcements with one
> system for discovering, joining, managing, and participating in every
> college club.**

### 60-second pitch

In our college, students discover academic and non-academic clubs
through different channels. Some clubs share Google Forms through email,
others use QR codes, WhatsApp groups, posters, or separate registration
links.

The problem does not end after registration. Students still need to find
event information, announcements, attendance records, and participation
history across different platforms.

Our solution is a **College Club Management System** that brings the
entire club ecosystem into one web application.

Students can discover clubs, view club details, apply for membership,
register for events, receive announcements, and track their attendance
and participation from a single dashboard.

Club coordinators get a dedicated dashboard to manage members, events,
registrations, attendance, announcements, and reports.

College administrators can monitor the overall club ecosystem using
analytics.

The long-term vision is to add AI-powered club and event recommendations
based on student interests and participation.

> **Instead of students searching across emails, QR codes, forms, and
> messaging groups, CCMS becomes the digital home for every college
> club.**

------------------------------------------------------------------------

# 2. Recommended technology stack

## Frontend

**React + TypeScript + Vite**

Why:

-   Component-based UI
-   Easy to learn and maintain
-   Excellent ecosystem
-   Good fit for dashboards
-   TypeScript reduces common coding mistakes
-   Vite provides a fast development environment

## UI

Recommended:

-   Tailwind CSS
-   shadcn/ui
-   Lucide React icons
-   Recharts for analytics

Use the component library consistently. Do not create a different visual
style for every page.

## Backend / Platform

**Supabase**

Supabase provides:

-   PostgreSQL database
-   Authentication
-   Row Level Security
-   Storage
-   Realtime capabilities
-   APIs generated from the database

This project does not need a traditional Express/Node backend for the
MVP.

## Deployment

**Vercel**

Use Vercel for the production frontend deployment.

## Source control

**Git + GitHub**

Git = version control on your computer.

GitHub = remote repository where your code is stored and shared.

Recommended workflow:

``` text
Your computer
     |
     | git commit
     v
    Git
     |
     | git push
     v
  GitHub
     |
     | automatic deployment
     v
  Vercel
```

## AI development environment

**Google Antigravity**

Use Antigravity as the agentic development environment.

Important rule:

> Do not ask the AI agent to build the entire production system blindly
> in one step.

Build in phases, verify each phase, then continue.

------------------------------------------------------------------------

# 3. Why React instead of plain HTML?

For this project, use:

> **React + TypeScript + Vite**

Do not build the full application using plain HTML/CSS/JavaScript.

Plain HTML is excellent for:

-   Simple static pages
-   Basic college websites
-   Small landing pages

But CCMS needs:

-   Authentication
-   Multiple dashboards
-   Role-based access
-   Dynamic club lists
-   Forms
-   Event registration
-   Attendance
-   Notifications
-   Database queries
-   Reusable components
-   State management

React is a better fit.

------------------------------------------------------------------------

# 4. High-level architecture

``` text
                         CCMS
                          |
             +------------+------------+
             |                         |
          Frontend                  Supabase
             |                         |
     React + TypeScript        +--------+--------+
             |                 |        |        |
          Vite               Auth   Database  Storage
             |                 |        |        |
             +-----------------+--------+--------+
                          |
                    PostgreSQL
                          |
                   Row Level Security
                          |
                    User Roles
                          |
        +-----------------+------------------+
        |                 |                  |
      Student          Coordinator          Admin
```

------------------------------------------------------------------------

# 5. User roles

The application must have three main roles.

## 5.1 Student

Students can:

-   Sign up/login
-   View clubs
-   Search/filter clubs
-   View club details
-   Apply for membership
-   View membership status
-   Register for events
-   View registered events
-   View attendance
-   Read announcements
-   View participation history
-   Manage profile

## 5.2 Club Coordinator

Coordinators can:

-   Access their club dashboard
-   Edit club information
-   Review membership applications
-   Approve/reject members
-   Create events
-   Edit/cancel events
-   View event registrations
-   Mark attendance
-   Create announcements
-   View club statistics

## 5.3 College Admin

Admins can:

-   Manage all clubs
-   Create/approve clubs
-   Assign coordinators
-   Manage users
-   View all events
-   View college-wide statistics
-   Manage categories
-   View reports
-   Control system-level settings

------------------------------------------------------------------------

# 6. MVP feature scope

Do not build every future feature immediately.

## Phase 1 --- MVP

### Authentication

-   Login
-   Sign up
-   Logout
-   Protected routes
-   Role detection

### Student

-   Dashboard
-   Club discovery
-   Club details
-   Join/apply
-   My clubs
-   Event registration
-   My events
-   Attendance
-   Announcements
-   Profile

### Coordinator

-   Dashboard
-   Club management
-   Membership approval
-   Event management
-   Registration list
-   Attendance management
-   Announcements

### Admin

-   Dashboard
-   Club management
-   User management
-   Coordinator management
-   Basic analytics

------------------------------------------------------------------------

# 7. Future features

Add these only after the MVP is stable.

## Version 2

-   QR event attendance
-   QR club membership
-   Certificate generation
-   Advanced analytics
-   Club activity timeline
-   Email notifications
-   Realtime notifications

## Version 3 --- AI layer

-   AI club recommendation
-   AI event recommendation
-   Student interest profiling
-   Club performance insights
-   AI club assistant
-   Natural-language search

Example:

> "Show me technical events happening this week."

The AI should query approved application data and return relevant
events.

Do not give an AI model unrestricted access to the database.

------------------------------------------------------------------------

# 8. Database design

Use PostgreSQL through Supabase.

Recommended tables:

``` text
profiles
clubs
club_memberships
events
event_registrations
attendance
announcements
notifications
club_categories
```

Optional later:

``` text
certificates
skills
student_interests
event_feedback
audit_logs
```

------------------------------------------------------------------------

# 9. Database relationships

``` text
profiles
   |
   +------< club_memberships >------ clubs
                                      |
                                      +------< events
                                                 |
                                                 +------< event_registrations
                                                 |
                                                 +------< attendance

clubs
   |
   +------< announcements

profiles
   |
   +------< event_registrations

profiles
   |
   +------< attendance
```

The important idea:

-   One student can join many clubs.
-   One club can have many students.
-   One club can create many events.
-   One event can have many registrations.
-   One event can have many attendance records.

------------------------------------------------------------------------

# 10. Suggested database fields

## profiles

``` text
id
full_name
email
student_id
department
year
phone
avatar_url
role
created_at
updated_at
```

Roles:

``` text
student
coordinator
admin
```

## clubs

``` text
id
name
slug
description
category_id
logo_url
cover_url
faculty_coordinator
student_coordinator
contact_email
status
created_at
updated_at
```

## club_categories

``` text
id
name
description
```

Examples:

``` text
Academic
Technical
Cultural
Social Service
Sports
Literary
Professional
Other
```

## club_memberships

``` text
id
student_id
club_id
status
applied_at
approved_at
joined_at
```

Status:

``` text
pending
approved
rejected
left
```

## events

``` text
id
club_id
title
description
event_date
start_time
end_time
venue
capacity
registration_open
registration_deadline
created_at
updated_at
```

## event_registrations

``` text
id
event_id
student_id
status
registered_at
```

## attendance

``` text
id
event_id
student_id
marked_at
status
```

Status:

``` text
present
absent
late
```

## announcements

``` text
id
club_id
title
content
published
created_at
updated_at
```

------------------------------------------------------------------------

# 11. Security model

Security is not optional.

Supabase credentials must be stored in environment variables.

Never put:

-   Service role key
-   Database password
-   Private API keys

inside frontend source code.

Use Supabase Row Level Security (RLS).

Example principle:

### Student

A student can read their own:

-   profile
-   memberships
-   event registrations
-   attendance

### Coordinator

A coordinator can manage only the club(s) they are assigned to.

### Admin

An admin can manage system-level data.

Do not solve authorization only with React UI checks.

A hidden button is not security.

The database policies must also enforce permissions.

------------------------------------------------------------------------

# 12. Project folder structure

Use a structure similar to:

``` text
college-club-management/
│
├── public/
│
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │   ├── ui/
│   │   ├── layout/
│   │   ├── clubs/
│   │   ├── events/
│   │   └── dashboard/
│   │
│   ├── pages/
│   │   ├── auth/
│   │   ├── student/
│   │   ├── coordinator/
│   │   └── admin/
│   │
│   ├── hooks/
│   │
│   ├── lib/
│   │   ├── supabase.ts
│   │   └── utils.ts
│   │
│   ├── services/
│   │   ├── clubs.ts
│   │   ├── events.ts
│   │   ├── memberships.ts
│   │   └── attendance.ts
│   │
│   ├── types/
│   │
│   ├── contexts/
│   │
│   ├── routes/
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
├── supabase/
│   ├── migrations/
│   └── seed.sql
│
├── .env.local
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

------------------------------------------------------------------------

# 13. UI/UX design direction

The exact visual theme should follow the reference website supplied for
this project.

If the reference is not available to Antigravity, do not invent a
completely different design. Ask the user to provide the reference
image/URL again.

## Design principles

The website should feel:

-   Modern
-   Premium
-   Clean
-   Academic but not boring
-   Professional
-   Responsive
-   Easy for first-year students
-   Dashboard-oriented

## Design consistency

Use one design system:

``` text
Typography
Colors
Spacing
Border radius
Shadows
Cards
Buttons
Forms
Tables
Navigation
Modal
Toast
```

Do not randomly change styles between pages.

## Responsive design

The application must work on:

-   Desktop
-   Laptop
-   Tablet
-   Mobile

Do not treat mobile as an afterthought.

------------------------------------------------------------------------

# 14. Main pages

## Public

``` text
/
 /clubs
 /clubs/:slug
 /events
 /login
 /register
```

## Student

``` text
/student/dashboard
/student/clubs
/student/my-clubs
/student/events
/student/attendance
/student/announcements
/student/profile
```

## Coordinator

``` text
/coordinator/dashboard
/coordinator/club
/coordinator/members
/coordinator/events
/coordinator/events/:id
/coordinator/attendance
/coordinator/announcements
/coordinator/analytics
```

## Admin

``` text
/admin/dashboard
/admin/clubs
/admin/users
/admin/coordinators
/admin/events
/admin/categories
/admin/reports
/admin/settings
```

------------------------------------------------------------------------

# 15. Student dashboard design

The dashboard should show:

``` text
Welcome back, Student 👋

My Clubs
[IEEE] [Music] [Rotaract]

Upcoming Events
-------------------------
AI Workshop
Oct 12
[View Event]

Club Announcements
-------------------------
IEEE announcement
NSS announcement

My Attendance
-------------------------
Overall: 87%

Quick Actions
[Explore Clubs]
[Upcoming Events]
[My Attendance]
```

------------------------------------------------------------------------

# 16. Club discovery page

Provide:

-   Search
-   Category filter
-   Department filter if required
-   Academic/non-academic filter
-   Club cards

Example:

``` text
Explore Clubs

Search clubs...

[All] [Academic] [Non-Academic]

------------------------------------------------

IEEE
Academic / Technical
Technology • Engineering

[View Club]

------------------------------------------------

Music Club
Cultural
Music • Performance

[View Club]
```

------------------------------------------------------------------------

# 17. Club details page

Include:

-   Club logo
-   Club cover
-   Name
-   Category
-   Description
-   Faculty coordinator
-   Student coordinator
-   Contact
-   Membership status
-   Upcoming events
-   Past events
-   Announcements
-   Join button

Membership button states:

``` text
JOIN CLUB
     ↓
PENDING
     ↓
APPROVED
```

------------------------------------------------------------------------

# 18. Event system

Every event should have:

``` text
Title
Club
Description
Date
Time
Venue
Capacity
Registration deadline
Registration status
```

Registration flow:

``` text
Student opens event
        ↓
Clicks Register
        ↓
System checks:
- logged in?
- already registered?
- registration open?
- deadline passed?
- capacity available?
        ↓
Registration created
        ↓
Student sees confirmation
```

------------------------------------------------------------------------

# 19. Attendance system

MVP:

Coordinator can manually mark:

``` text
Present
Absent
Late
```

Later:

### QR attendance

``` text
Coordinator creates attendance session
            ↓
System generates QR
            ↓
Student scans QR
            ↓
Authenticated student is identified
            ↓
System validates event/session
            ↓
Attendance recorded
```

Important:

Do not rely only on a static QR code.

For a real system, use:

-   authenticated users
-   short-lived attendance sessions
-   server/database validation
-   duplicate prevention

------------------------------------------------------------------------

# 20. Notifications

Initial version:

-   In-app notifications

Later:

-   Email notifications
-   Push notifications

Examples:

``` text
Your IEEE membership was approved.

Your AI Workshop registration is confirmed.

NSS announced a new volunteering event.

Your attendance has been marked.
```

------------------------------------------------------------------------

# 21. Analytics

Student analytics:

``` text
Clubs joined
Events registered
Events attended
Attendance percentage
Participation hours
```

Coordinator analytics:

``` text
Total members
Pending applications
Event registrations
Event attendance
Attendance percentage
Membership growth
```

Admin analytics:

``` text
Total clubs
Academic clubs
Non-academic clubs
Total students
Total memberships
Events this month
Most active clubs
Overall participation
```

Use charts only where they improve understanding.

------------------------------------------------------------------------

# 22. AI roadmap

Do not implement AI during the first database/authentication phase.

After the core system works:

## AI Feature 1 --- Club Recommendation

Input:

``` text
Student interests
Department
Skills
Previous clubs
Events attended
```

Output:

``` text
Recommended Clubs

1. IEEE       94%
2. AI Club    91%
3. Coding     88%
```

## AI Feature 2 --- Event Recommendation

Recommend events based on:

-   interests
-   memberships
-   previous participation

## AI Feature 3 --- Club Assistant

Example:

> "What technical events are happening this month?"

The assistant should retrieve data from approved application sources
before generating the response.

------------------------------------------------------------------------

# 23. Antigravity development procedure

Google Antigravity is an agentic development environment. Treat the
agent like a developer working with you, not like a magic website
generator.

## Golden rule

Build in small, verifiable milestones.

Do:

``` text
Plan
↓
Implement
↓
Run
↓
Test
↓
Review
↓
Commit
↓
Next phase
```

Do NOT do:

``` text
"Build my entire application"
↓
Accept everything
↓
Hope it works
```

------------------------------------------------------------------------

# 24. Step 1 --- Install prerequisites

Install:

-   Node.js LTS
-   Git
-   Google Antigravity
-   GitHub account
-   Supabase account
-   Vercel account

Verify Node:

``` bash
node --version
```

Verify npm:

``` bash
npm --version
```

Verify Git:

``` bash
git --version
```

------------------------------------------------------------------------

# 25. Step 2 --- Create the project

Recommended:

``` bash
npm create vite@latest college-club-management -- --template react-ts
```

Then:

``` bash
cd college-club-management
npm install
npm run dev
```

Open the local URL shown by Vite.

Usually:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# 26. Step 3 --- Open the project in Antigravity

Open the project folder:

``` text
college-club-management
```

Do not create the project in a random temporary folder.

The root should contain:

``` text
package.json
src/
public/
vite.config.ts
```

------------------------------------------------------------------------

# 27. Step 4 --- Install frontend dependencies

Recommended:

``` bash
npm install @supabase/supabase-js
npm install react-router-dom
npm install lucide-react
npm install recharts
```

For Tailwind/shadcn, follow the current official installation
instructions for the versions generated by your Vite project.

Do not copy an old Tailwind setup blindly if the current tooling has
changed.

------------------------------------------------------------------------

# 28. Step 5 --- Create Git repository

From the project root:

``` bash
git init
git add .
git commit -m "Initial project setup"
```

Create a GitHub repository named:

``` text
college-club-management
```

Then connect it:

``` bash
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace the placeholder with your actual GitHub repository URL.

------------------------------------------------------------------------

# 29. Step 6 --- Create Supabase project

Create a new Supabase project.

Save:

``` text
Project URL
Publishable key
```

Create:

``` text
.env.local
```

Example:

``` env
VITE_SUPABASE_URL=your-project-url
VITE_SUPABASE_PUBLISHABLE_KEY=your-publishable-key
```

Never commit `.env.local`.

Your `.gitignore` must include:

``` text
.env
.env.local
.env.*.local
```

Keep a safe example:

``` text
.env.example
```

with:

``` env
VITE_SUPABASE_URL=
VITE_SUPABASE_PUBLISHABLE_KEY=
```

------------------------------------------------------------------------

# 30. Step 7 --- Connect Supabase

Create:

``` text
src/lib/supabase.ts
```

The client should read environment variables.

Conceptually:

``` ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY
)
```

Do not hard-code credentials.

------------------------------------------------------------------------

# 31. Step 8 --- Build database before complex UI

Create the database schema first.

Recommended order:

``` text
1. profiles
2. club_categories
3. clubs
4. club_memberships
5. events
6. event_registrations
7. attendance
8. announcements
9. notifications
```

Then create:

-   Primary keys
-   Foreign keys
-   Unique constraints
-   Indexes
-   RLS policies

Do not start with fake frontend data and forget the database
architecture.

------------------------------------------------------------------------

# 32. Step 9 --- Authentication

Start with:

-   Email/password authentication

Later you may add:

-   College email restriction
-   Magic link
-   Google OAuth
-   College SSO

For the first version, email/password is simpler.

After signup:

``` text
auth.users
     ↓
profiles
     ↓
role
```

A user must have a profile record.

------------------------------------------------------------------------

# 33. Step 10 --- Role-based routing

After authentication:

``` text
role = student
      ↓
/student/dashboard

role = coordinator
      ↓
/coordinator/dashboard

role = admin
      ↓
/admin/dashboard
```

Protected routes must prevent unauthorized access.

Example:

A student must not be able to access:

``` text
/admin/users
```

Changing the URL manually must not bypass database security.

------------------------------------------------------------------------

# 34. Step 11 --- Build features in this order

Use this exact order.

### Milestone 1

``` text
Project setup
GitHub
Supabase connection
Basic UI
```

### Milestone 2

``` text
Authentication
Profiles
Roles
Protected routes
```

### Milestone 3

``` text
Club categories
Clubs
Club discovery
Club details
```

### Milestone 4

``` text
Membership applications
Approval workflow
My clubs
```

### Milestone 5

``` text
Events
Event registration
My events
```

### Milestone 6

``` text
Attendance
Attendance dashboard
```

### Milestone 7

``` text
Announcements
Notifications
```

### Milestone 8

``` text
Coordinator dashboard
```

### Milestone 9

``` text
Admin dashboard
```

### Milestone 10

``` text
Analytics
Responsive polishing
Security review
Testing
```

### Milestone 11

``` text
QR attendance
```

### Milestone 12

``` text
AI recommendations
AI assistant
```

------------------------------------------------------------------------

# 35. Git workflow

After every working milestone:

``` bash
git status
git add .
git commit -m "feat: add authentication"
git push
```

Example commits:

``` text
feat: initialize react application
feat: connect supabase
feat: add authentication
feat: add role based routing
feat: add club discovery
feat: add membership workflow
feat: add event registration
feat: add attendance
feat: add announcements
feat: add coordinator dashboard
feat: add admin dashboard
fix: correct membership approval policy
style: improve responsive dashboard
```

Do not wait until the entire project is finished before pushing to
GitHub.

------------------------------------------------------------------------

# 36. Testing checklist

Before considering a feature complete:

## Authentication

-   [ ] Valid signup works
-   [ ] Invalid email handled
-   [ ] Wrong password handled
-   [ ] Logout works
-   [ ] Protected route works
-   [ ] Role routing works

## Clubs

-   [ ] Clubs load
-   [ ] Search works
-   [ ] Filters work
-   [ ] Club detail works
-   [ ] Join button works
-   [ ] Duplicate membership prevented

## Events

-   [ ] Event creation works
-   [ ] Event list works
-   [ ] Registration works
-   [ ] Duplicate registration prevented
-   [ ] Capacity enforced
-   [ ] Deadline enforced

## Attendance

-   [ ] Coordinator can mark attendance
-   [ ] Student can see attendance
-   [ ] Duplicate attendance prevented

## Security

-   [ ] Student cannot access admin data
-   [ ] Student cannot modify another student's data
-   [ ] Coordinator cannot modify another club
-   [ ] RLS policies tested
-   [ ] Secret keys are not committed

------------------------------------------------------------------------

# 37. Deployment to Vercel

Push the working application to GitHub.

Then:

1.  Open Vercel.
2.  Import the GitHub repository.
3.  Select the React/Vite project.
4.  Add environment variables.
5.  Deploy.

Environment variables:

``` text
VITE_SUPABASE_URL
VITE_SUPABASE_PUBLISHABLE_KEY
```

Do not put secrets directly into source code.

After deployment:

``` text
GitHub push
     ↓
Vercel build
     ↓
Production deployment
```

Every future push to the connected production branch can trigger a new
deployment.

------------------------------------------------------------------------

# 38. Supabase production checklist

Before public deployment:

-   [ ] RLS enabled on every private table
-   [ ] Policies reviewed
-   [ ] No service-role key in frontend
-   [ ] Authentication settings reviewed
-   [ ] Storage policies reviewed
-   [ ] Database constraints tested
-   [ ] Duplicate registrations prevented
-   [ ] Role permissions tested

The frontend is not your security boundary.

The database policies are critical.

------------------------------------------------------------------------

# 39. Antigravity master prompt

Use the following prompt as the main starting prompt in Antigravity.

------------------------------------------------------------------------

## MASTER PROMPT --- COPY THIS INTO ANTIGRAVITY

``` text
You are the lead full-stack engineer and UI/UX architect for my project.

PROJECT NAME:
College Club Management System (CCMS)

PROJECT PURPOSE:
Build a production-quality web application that centralizes all academic and non-academic college clubs into one platform.

CURRENT REAL-WORLD PROBLEM:
In my college, students currently discover and register for clubs through scattered channels such as Google Forms shared through email, QR codes, WhatsApp messages, posters, and separate registration links.

Academic clubs and non-academic clubs use different registration methods.

Students also struggle to track:
- Which clubs they joined
- Membership status
- Upcoming activities
- Event registrations
- Attendance
- Announcements
- Participation history

The goal is to create one centralized platform.

CORE PRODUCT IDEA:
"One platform. Every club. Every student. Every activity."

TECH STACK:
- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui where appropriate
- Lucide React
- React Router
- Recharts
- Supabase
- PostgreSQL
- Supabase Auth
- Supabase Storage where required
- Supabase Row Level Security
- Git
- GitHub
- Vercel

IMPORTANT:
Do not replace React with plain HTML.
Do not introduce a traditional Express backend unless there is a specific requirement that cannot be safely handled with Supabase.
Use Supabase as the backend platform.

USERS:
1. Student
2. Club Coordinator
3. College Admin

STUDENT FEATURES:
- Authentication
- Student profile
- Discover clubs
- Search clubs
- Filter clubs
- View club details
- Apply for membership
- View membership status
- View joined clubs
- View upcoming events
- Register for events
- View registered events
- View attendance
- View announcements
- View participation history

COORDINATOR FEATURES:
- Coordinator dashboard
- Club profile management
- View membership applications
- Approve/reject membership
- Member management
- Create events
- Edit events
- Cancel events
- View event registrations
- Manage attendance
- Publish announcements
- Club analytics

ADMIN FEATURES:
- Admin dashboard
- Manage clubs
- Create clubs
- Approve clubs
- Manage categories
- Manage users
- Assign coordinators
- View events
- View college-wide analytics
- Reports
- System settings

DATABASE TABLES:
- profiles
- club_categories
- clubs
- club_memberships
- events
- event_registrations
- attendance
- announcements
- notifications

OPTIONAL FUTURE TABLES:
- certificates
- student_interests
- event_feedback
- audit_logs

DATABASE SECURITY:
Use PostgreSQL constraints, foreign keys, indexes and Supabase Row Level Security.

Never depend only on frontend checks for authorization.

STUDENT:
Students may access their own profile, memberships, registrations, attendance and notifications.

COORDINATOR:
A coordinator can manage only the club(s) assigned to them.

ADMIN:
Admins can manage system-level resources.

Never expose service-role credentials to the browser.

AUTHENTICATION:
Use Supabase Auth.

Start with email/password authentication.

Create a profiles record associated with the authenticated user.

ROUTING:
Public:
/
 /clubs
 /clubs/:slug
 /events
 /login
 /register

Student:
 /student/dashboard
 /student/clubs
 /student/my-clubs
 /student/events
 /student/attendance
 /student/announcements
 /student/profile

Coordinator:
 /coordinator/dashboard
 /coordinator/club
 /coordinator/members
 /coordinator/events
 /coordinator/attendance
 /coordinator/announcements
 /coordinator/analytics

Admin:
 /admin/dashboard
 /admin/clubs
 /admin/users
 /admin/coordinators
 /admin/events
 /admin/categories
 /admin/reports
 /admin/settings

UI/UX:
The visual theme must closely follow the reference website/image supplied by the user.

If the reference is not accessible in the current context, DO NOT invent a completely different visual language. Tell me that the reference is unavailable and ask me to provide it.

The final UI should be:
- Modern
- Premium
- Clean
- Professional
- Academic
- Responsive
- Accessible
- Consistent

Use:
- Reusable components
- Consistent spacing
- Consistent typography
- Consistent buttons
- Consistent cards
- Consistent forms
- Consistent tables
- Consistent navigation
- Responsive layouts

Do not create unnecessary visual complexity.

ARCHITECTURE:
Keep business logic separate from UI.

Prefer:
src/
  components/
  pages/
  hooks/
  lib/
  services/
  types/
  contexts/
  routes/

Create reusable service functions for Supabase operations.

Do not place large amounts of database logic directly inside UI components.

DATABASE DEVELOPMENT:
Before implementing complicated UI, establish the database schema.

Create:
- tables
- relationships
- indexes
- constraints
- RLS policies

Use generated TypeScript database types when practical.

MVP DEVELOPMENT ORDER:

PHASE 1:
Project setup
React + TypeScript + Vite
Git
GitHub
Supabase connection
Basic design system

PHASE 2:
Authentication
Profiles
Roles
Protected routes

PHASE 3:
Club categories
Club discovery
Club details

PHASE 4:
Membership workflow

PHASE 5:
Events
Event registration

PHASE 6:
Attendance

PHASE 7:
Announcements
Notifications

PHASE 8:
Coordinator dashboard

PHASE 9:
Admin dashboard

PHASE 10:
Analytics
Responsive polishing
Testing
Security review

PHASE 11:
QR attendance

PHASE 12:
AI features

AI FEATURES ARE FUTURE FEATURES.
Do not add AI before the core system is stable.

FUTURE AI:
1. Club recommendations
2. Event recommendations
3. AI club assistant
4. Natural language event search
5. Club engagement insights

AI must not receive unrestricted database access.

DEVELOPMENT RULE:
Work incrementally.

For each phase:
1. Explain what you are going to change.
2. Inspect the existing project.
3. Implement only that phase.
4. Run the application.
5. Run relevant checks/tests.
6. Fix errors.
7. Summarize changed files.
8. Tell me exactly how to test the phase.
9. Wait for my approval before moving to the next major phase.

Do not overwrite working functionality unnecessarily.

Do not rewrite the whole project to fix a small bug.

When modifying existing files, preserve working functionality.

ERROR HANDLING:
Do not hide errors.

Use clear:
- loading states
- empty states
- success messages
- error messages
- validation messages

Never leave buttons that silently fail.

FORM VALIDATION:
Validate required fields.
Validate email.
Validate dates.
Validate event capacity.
Prevent duplicate memberships.
Prevent duplicate event registration.

ACCESSIBILITY:
Use:
- semantic HTML
- keyboard accessible controls
- labels
- meaningful button text
- sufficient contrast
- visible focus states
- accessible dialogs

RESPONSIVENESS:
Test desktop, tablet and mobile layouts.

GITHUB:
Keep commits logical.

Suggested commit messages:
feat: initialize project
feat: add authentication
feat: add role based routing
feat: add club discovery
feat: add membership workflow
feat: add events
feat: add attendance
feat: add announcements
feat: add coordinator dashboard
feat: add admin dashboard
fix: ...
style: ...

ENVIRONMENT VARIABLES:
Use .env.local.

Expected variables:
VITE_SUPABASE_URL=
VITE_SUPABASE_PUBLISHABLE_KEY=

Never commit .env.local.

Create .env.example with empty placeholders.

DEPLOYMENT:
The application will be deployed to Vercel from GitHub.

Production environment variables must be configured in Vercel.

Do not put secrets in source code.

CODE QUALITY:
Use TypeScript properly.
Avoid any unless truly necessary.
Create meaningful names.
Avoid duplicate code.
Create reusable components.
Keep components reasonably small.
Add comments only when they explain non-obvious decisions.

IMPORTANT PRODUCT RULE:
This is a real college club management system, not just a demo landing page.

The application must have functional:
- authentication
- database operations
- memberships
- events
- attendance
- role permissions

Do not fake core functionality with static arrays once Supabase is connected.

SEED DATA:
Create realistic development seed data for:
- several academic clubs
- several non-academic clubs
- sample events
- sample announcements

Clearly label seed/demo data.

Do not use real student personal information.

FIRST TASK:
Do not immediately generate the entire application.

First:
1. Inspect the current workspace.
2. Create a project architecture plan.
3. Identify whether the project is empty or already contains code.
4. Present the proposed folder structure.
5. Present the database schema plan.
6. Present the authentication/authorization plan.
7. Present the UI page map.
8. Present the implementation milestones.

Then wait for approval.

After approval, implement Phase 1 only.
```

------------------------------------------------------------------------

# 40. Prompts to use after the master prompt

Do not repeatedly paste the huge master prompt.

Use smaller prompts.

## Authentication prompt

``` text
Implement Phase 2 authentication only.

Use Supabase Auth.

Requirements:
- signup
- login
- logout
- session persistence
- profiles table integration
- role-based routing
- protected routes
- loading states
- error states

Roles:
student
coordinator
admin

Do not implement clubs, events or attendance yet.

After implementation:
1. run the app
2. test signup
3. test login
4. test logout
5. test protected routes
6. verify role routing
7. report changed files
8. report any errors
```

## Club prompt

``` text
Implement the club discovery and club details module.

Requirements:
- club categories
- club listing
- search
- filters
- club cards
- club details page
- responsive UI
- Supabase database integration

Do not implement event registration yet.

Use real Supabase data rather than hardcoded arrays after the database is connected.

Test:
- search
- category filter
- open club
- loading state
- empty state
- error state
- mobile layout
```

## Membership prompt

``` text
Implement the club membership workflow.

Student:
- Apply to join
- View pending status
- View approved clubs
- Prevent duplicate applications

Coordinator:
- View applications
- Approve
- Reject
- View members

Security:
- Student can modify only their own application
- Coordinator can manage only assigned clubs
- Enforce permissions using Supabase RLS

Do not implement events yet.
```

## Event prompt

``` text
Implement the event module.

Student:
- view events
- view event details
- register
- view registered events

Coordinator:
- create event
- edit event
- cancel event
- view registrations

Rules:
- prevent duplicate registration
- enforce capacity
- enforce registration deadline
- show clear errors
- show loading states

Do not implement QR attendance yet.
```

## Attendance prompt

``` text
Implement attendance management.

MVP:
- coordinator can view event participants
- coordinator can mark present/absent/late
- student can view attendance
- calculate attendance percentage
- prevent duplicate attendance

Do not implement QR attendance in this phase.

After the manual attendance system works, we will build QR attendance separately.
```

## UI polishing prompt

``` text
Audit the entire current UI against the project's design reference.

Do not change functionality.

Check:
- spacing
- typography
- colors
- cards
- buttons
- navigation
- forms
- tables
- responsive layout
- loading states
- empty states
- error states
- accessibility

Reuse existing design tokens/components.

Do not introduce unnecessary visual effects.

After changes, test desktop, tablet and mobile.
```

------------------------------------------------------------------------

# 41. How to use Antigravity effectively

Use this pattern:

``` text
YOU:
"Implement Phase 1 only."

ANTIGRAVITY:
Builds Phase 1

YOU:
"Test it."

ANTIGRAVITY:
Tests

YOU:
"Fix the error."

ANTIGRAVITY:
Fixes

YOU:
"Explain what changed."

ANTIGRAVITY:
Explains

YOU:
"Commit this milestone."

ANTIGRAVITY:
Prepares commit

YOU:
"Move to Phase 2."
```

This gives you much more control.

------------------------------------------------------------------------

# 42. If Antigravity creates an error

Do not immediately ask it to rewrite the project.

Give the exact error.

Use:

``` text
I encountered this error:

[PASTE COMPLETE ERROR]

Do not rewrite unrelated parts of the project.

First identify:
1. root cause
2. affected file
3. why it happened
4. smallest safe fix

Then implement the fix and test it.
```

------------------------------------------------------------------------

# 43. If you don't understand generated code

Ask:

``` text
Explain this implementation as if I am a beginner learning React and Supabase.

Explain:
1. What this file does
2. Why this file exists
3. What each important function does
4. How data moves from React to Supabase
5. What happens when the user clicks the button
6. What security rule protects this operation

Do not rewrite the code.
Teach me the code.
```

This turns the project into a learning resource instead of simply an
AI-generated project.

------------------------------------------------------------------------

# 44. How to learn the project later

If you return to this project after several months, start here:

``` text
1. Read this README
2. Understand the architecture
3. Open package.json
4. Open src/App.tsx
5. Open src/main.tsx
6. Open src/lib/supabase.ts
7. Open routes
8. Open pages
9. Open services
10. Open database migrations
```

Then ask Antigravity:

``` text
I am learning this project again.

Do not modify anything.

Explain the architecture from the browser to Supabase.

Start with:
React
→ routing
→ authentication
→ components
→ services
→ Supabase
→ PostgreSQL
→ RLS

Then explain one complete user flow:
Student logs in
→ opens a club
→ applies for membership
→ coordinator approves
→ student sees approved membership.

Explain it as a beginner tutorial.
```

------------------------------------------------------------------------

# 45. Recommended learning order for you

Do not try to learn everything simultaneously.

Learn:

``` text
HTML
 ↓
CSS
 ↓
JavaScript
 ↓
TypeScript basics
 ↓
React
 ↓
React Router
 ↓
Supabase
 ↓
PostgreSQL basics
 ↓
Authentication
 ↓
RLS
 ↓
Git
 ↓
GitHub
 ↓
Vercel
 ↓
Testing
 ↓
AI integration
```

You do not need to become an expert in every technology before starting.

Build the application while learning.

------------------------------------------------------------------------

# 46. Git/GitHub reminder

Remember:

### Git

Runs on your computer.

``` text
git add
git commit
git branch
git log
```

### GitHub

Online repository.

``` text
git push
git pull
```

### Vercel

Deployment platform.

``` text
GitHub
   ↓
Vercel
   ↓
Live website
```

------------------------------------------------------------------------

# 47. Recommended final project roadmap

``` text
WEEK 1
Project setup
React
TypeScript
Git
GitHub
Supabase

WEEK 2
Authentication
Profiles
Roles
RLS

WEEK 3
Club discovery
Club profiles
Membership

WEEK 4
Events
Registration

WEEK 5
Attendance
Announcements

WEEK 6
Coordinator dashboard
Admin dashboard

WEEK 7
Analytics
Responsive UI
Testing

WEEK 8
QR attendance
Deployment
Documentation

AFTER MVP
AI recommendations
AI assistant
Advanced analytics
```

The exact timeline can change. Quality is more important than speed.

------------------------------------------------------------------------

# 48. Definition of done

The MVP is complete only when:

``` text
[ ] Student can register/login
[ ] Student profile works
[ ] Roles work
[ ] Clubs are stored in Supabase
[ ] Students can discover clubs
[ ] Students can apply to clubs
[ ] Coordinators can approve members
[ ] Students can see memberships
[ ] Coordinators can create events
[ ] Students can register for events
[ ] Duplicate registration is prevented
[ ] Attendance works
[ ] Students can view attendance
[ ] Announcements work
[ ] Coordinator dashboard works
[ ] Admin dashboard works
[ ] RLS is configured
[ ] Responsive design works
[ ] GitHub repository is clean
[ ] Production environment variables are configured
[ ] Vercel deployment works
[ ] No secrets are committed
[ ] Core flows have been tested
```

------------------------------------------------------------------------

# 49. Final product vision

The first version:

``` text
Club Registration System
```

The mature version:

``` text
                    COLLEGE CLUB OS
                          |
       +------------------+------------------+
       |                  |                  |
    Students          Coordinators         Admin
       |                  |                  |
    Discover            Manage              Monitor
    Join                Events              Analytics
    Register            Members             Reports
    Attend              Attendance
    Track               Announce
       |                  |
       +------------------+
                |
             AI Layer
                |
       +--------+--------+
       |        |        |
    Recommend  Search  Insights
```

The long-term objective is to create a platform that the college could
realistically use instead of maintaining separate registration forms and
spreadsheets for every club.

------------------------------------------------------------------------

# 50. Important project principle

Do not measure the success of this project by:

> "How many technologies did I use?"

Measure it by:

> "How many real college club problems does this system solve reliably?"

A clean React + Supabase application with strong authentication,
database design, RLS, membership workflows, events and attendance is
better than a huge application filled with unnecessary AI features.

Build the foundation first.

Then make it intelligent.

------------------------------------------------------------------------

# 51. Official documentation to keep bookmarked

-   Google Antigravity documentation/codelabs
-   React documentation
-   Vite documentation
-   Supabase documentation
-   Supabase Auth documentation
-   PostgreSQL documentation
-   Git documentation
-   GitHub documentation
-   Vercel documentation

When a tool changes, prefer the current official documentation over old
tutorials.

------------------------------------------------------------------------

# 52. Project completion checklist

Before your final college demonstration:

### Product

-   [ ] Problem clearly demonstrated
-   [ ] Solution clearly demonstrated
-   [ ] Student workflow demonstrated
-   [ ] Coordinator workflow demonstrated
-   [ ] Admin workflow demonstrated

### Technical

-   [ ] React + TypeScript
-   [ ] Supabase
-   [ ] PostgreSQL
-   [ ] Auth
-   [ ] RLS
-   [ ] GitHub
-   [ ] Vercel

### Demo

Show this flow:

``` text
Student Login
      ↓
Explore Clubs
      ↓
Open IEEE
      ↓
Apply
      ↓
Coordinator Login
      ↓
Approve Student
      ↓
Student Login
      ↓
Membership Approved
      ↓
Open Event
      ↓
Register
      ↓
Coordinator Marks Attendance
      ↓
Student Views Attendance
```

That single flow demonstrates the core value of the entire system.

------------------------------------------------------------------------

## End of README

**Project identity:**

> # CCMS --- College Club Management System
>
> **One platform. Every club. Every student. Every activity.**
