# CCMS — College Club Management System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel%20Production-success?logo=vercel&logoColor=white)](https://club-management-system-pi.vercel.app)
[![Vite](https://img.shields.io/badge/Vite-8.3-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com/)
[![Tests](https://img.shields.io/badge/Pytest-30%20Passed%20(100%25)-brightgreen?logo=pytest&logoColor=white)](./TESTING/)

> A streamlined, accessible collegiate platform connecting ambitious students with departmental faculty mentors for club discovery, weekly activity scheduling, department-wise sorting, and institutional attendance accreditation.

---

## Key Features

- **Strictly Two Roles**: Direct peer-to-mentor collaboration between **Students** and **Faculty Coordinators** without administrative bottlenecks.
- **Club Catalogs & Applications**: Filter clubs across Tech, Robotics, Design, Cultural, and Sports domains, and submit joining applications directly to faculty leads.
- **Department-Wise Applicant Sorting**: Faculty coordinators view and manage applicants organized by academic department (CSE, ECE, Mechanical, Visual Arts).
- **Colorful Email Acceptance Notifications**: Automated, officially branded welcome emails dispatched to students upon coordinator approval.
- **Weekly Activity Time Table**: Synchronized schedules with venue room numbers, timings, session descriptions, and seat reservations.
- **Digital Session Attendance**: Verified attendance roll calls and transcripts for co-curricular accreditation.
- **High-Contrast Dark & Light Mode**: Accessible, adaptive UI with sharp text contrast across both visual modes.
- **Comprehensive 30-Test Suite**: Pytest test suite covering positive, negative, boundary, functional, integration, and validation error scenarios with a 100% pass rate.

---

## Documentation

- **[USER MANUAL (Comprehensive Guide)](./USER_MANUAL.md)**: Detailed operational guide, dual-role workflows, email templates, and step-by-step instructions.
- **[Software Requirements Specification (SRS)](./docs/SRS.md)**: Full IEEE 830 compliant SRS document.
- **[UML Diagrams Specification](./docs/UML_DIAGRAMS.md)**: System architecture, Class diagram, Use Case, Sequence, State, and Component diagrams.
- **[Automated Testing Report](./TESTING/)**: Pytest verification logs and boundary tests.

---

## Quick Start

### 1. Installation
```bash
git clone https://github.com/NAVXXN0611/Club-Management-System-.git
cd Club-Management-System-
npm install
```

### 2. Environment Variables
Create `.env.local` in the project root:
```env
VITE_SUPABASE_URL=https://parjnyhhwobbybxvtyah.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=sb_publishable_VJhDbMNa7KJTSIXRWyD3Xw_YdJbAzkM
```

### 3. Run Development Server
```bash
npm run dev
```
Open [http://localhost:5173/](http://localhost:5173/) in your browser.

### 4. Run Automated Pytest Tests
```bash
python -m pytest TESTING/ -v
```

### 5. Production Build
```bash
npm run build
```

---

## Deployment (Vercel)

The application includes [`vercel.json`](./vercel.json) for instant global edge deployment with SPA routing support:

```bash
vercel --prod
```

---

## License

This project is licensed under the MIT License.
