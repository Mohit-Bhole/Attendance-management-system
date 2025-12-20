# Smart Attendance Management System

A web-based attendance system developed as a final year capstone project to digitize and streamline attendance tracking.

## Team Members
- **Vikas Gaikwad (Group Leader):** UI Design & Flask Integration
- **Vedant Shivade:** Frontend Development & Templates
- **Rushad Adikane:** Database & Backend Logic
- **Divesh More:** Testing & Documentation

## Guided by
- Megha Shinde (HOD)

## Subjects Involved
- Network and Info Security – Saloni Purkar
- Mobile App Dev – Jyoti Chandwade
- Class Advisor – Ashwini Patil

## Features
- Role-based access control (Admin, Teacher, Student)
- Real-time attendance tracking
- Automated reports
- Dashboard interfaces for different user roles
- Attendance status visualization
- Export reports to CSV

## Tech Stack
- Backend: Python with Flask framework
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Styling: Bootstrap 5
- Icons: Bootstrap Icons

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/Mohit-Bhole/Attendance-management-system.git
   cd attendance-management-system
   ```

2. Create and activate a virtual environment (recommended):
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Access the application at: `http://localhost:5000`

## Default Login Credentials

### Admin
- Username: MeghaShinde
- Password: admin123

### Teachers
| Name            | Subject                  | Username | Password |
|-----------------|--------------------------|----------|----------|
| Saloni Purkar   | Network & Info Security | saloni   | teach123 |
| Ashwini Patil   | Class Teacher           | ashwini  | teach456 |
| Jyoti Chandwade | Mobile App Dev          | jyoti    | teach789 |

### Students
| Name            | Username | Password |
|-----------------|----------|----------|
| Vikas Gaikwad   | vikas    | stud123  |
| Vedant Shivade  | vedant   | stud456  |
| Rushad Adikane  | rushad   | stud789  |
| Divesh More     | divesh   | stud101  |

## Project Structure
```
attendance-system/
├── app.py               # Main Flask application
├── database.db          # SQLite database (created on first run)
├── requirements.txt     # Python dependencies
├── schema.sql           # Database schema
├── static/              # Static files
│   ├── css/             # CSS stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Images and icons
└── templates/           # HTML templates
    ├── base.html        # Base template with common structure
    ├── index.html       # Landing page
    ├── login.html       # Login page
    └── ... (other templates)
```
---

**BUILT BY - MOHIT BHOLE**

---
## License

This project is created as a capstone project for educational purposes. 

