# 🎟️ Church Raffle Management System

A modern, secure, and easy-to-use **Django-based raffle management system** designed for churches, youth ministries, and community fundraising events.  
This system simplifies payment tracking, ticket generation, and winner selection while ensuring transparency and accountability.

---

## 📌 Project Overview

The Church Raffle Management System automates the entire raffle process:

- Members make payments via **M-Pesa Paybill**
- Payment messages are forwarded to the church secretary
- Secretary uploads/pastes the M-Pesa SMS into the system
- The system automatically extracts payment details
- Tickets are generated and assigned to participants
- Admin dashboard tracks all sales in real time
- Winners are selected fairly during the draw

---

## 🚀 Key Features

### 💳 Payment Processing
- Supports M-Pesa Paybill workflow
- Manual message entry (copy/paste SMS)
- Automatic extraction of:
  - Customer name
  - Amount paid
  - M-Pesa reference code
  - Timestamp

---

### 🎫 Ticket Management
- Automatic ticket generation based on payment amount
- Unique sequential ticket numbers
- Ticket ownership linked to users
- Printable ticket support (PDF)

---

### 📊 Admin Dashboard
- Real-time sales tracking
- Total revenue overview
- Ticket statistics (sold, pending, printed)
- Search payments and tickets
- Export data to Excel/PDF

---

### 🏆 Transparent Draw System
- Random winner selection from valid paid tickets
- Prevent duplicate winners (configurable)
- Audit trail for fairness
- Live draw display for events

---

### 🖨️ Ticket Printing
- Clean printable ticket design
- Supports batch printing
- Includes:
  - Ticket number
  - Name
  - Reference code
  - Event details

---

## 🏗️ System Workflow
Member Pays via Paybill
↓
M-Pesa SMS Received
↓
Message Forwarded to Secretary
↓
Secretary Pastes Message into System
↓
System Extracts Payment Data
↓
Tickets Automatically Generated
↓
Stored in Database
↓
Ready for Draw & Printing


---

## 🛠️ Tech Stack

### Backend
- Django
- Django REST Framework (optional API layer)

### Database
- PostgreSQL / SQLite (development)

### Frontend
- Django Templates OR React (optional upgrade)
- Bootstrap / Tailwind CSS

### Utilities
- Regex (for SMS parsing)
- WeasyPrint / ReportLab (PDF ticket generation)

---

## 🗂️ Database Structure

### Members
- id
- name
- phone

### Payments
- id
- mpesa_reference
- amount
- message_text
- status

### Tickets
- id
- ticket_number
- member_id
- payment_id
- status (generated/printed/collected)

### Draws
- id
- date
- winner_ticket
- prize_name

---

## 🎯 Use Case

This system is designed for:

- Church fundraising events
- Youth ministry raffles
- School fundraising draws
- Community charity events

---

## 🔐 Transparency & Fairness

- Every ticket is tied to a verified payment
- Full audit trail of all transactions
- Randomized draw ensures fairness
- No manual interference in winner selection

---

## 📈 Future Improvements

- Direct M-Pesa Daraja API integration
- SMS automation via Africa’s Talking
- QR code ticket verification
- Online self-service ticket purchase portal
- Mobile app version

---

## 🧑‍💻 Installation (Developer Setup)

```bash
git clone https://github.com/your-org/raffle-system.git
cd raffle-system

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
