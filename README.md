# LogRegs - Multi-Tenant Expense Tracker

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2.4-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16.0-blue?logo=django&logoColor=white)

---

## About The Project

**LogRegs** is a Django-based multi-tenant expense tracking application that allows multiple admins to manage their own users and expenses independently. Each admin-user group (tenant) has fully isolated data to ensure privacy and security.

The app provides admins the ability to perform CRUD operations on users and expenses, and users can manage their own expenses. Live charts help visualize expenses for better tracking and analysis.  

---

## Features

### Admin
- Register and manage users under their tenant.
- View, add, edit, and delete expenses for all users in their group.
- Monitor live charts of expenses.

### Users
- Add, update, and delete their own expenses.
- View personal expense history and charts.

### Common
- Authentication and role-based access.
- Multi-tenant separation ensures data isolation.
- Frontend implemented using HTML, CSS, and JavaScript for responsive UI.

---
## Support Developer

1. Add a Star 🌟 to this 👆 Repository

## How to Install and Run this project?

### Pre-Requisites:

1. Install Git Version Control
   [ https://git-scm.com/ ]

2. Install Python Latest Version
   [ https://www.python.org/downloads/ ]

3. Install Pip (Package Manager)
   [ https://pip.pypa.io/en/stable/installing/ ]

### Installation

**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First

```
$  pip install virtualenv
```

Create Virtual Environment

For Windows

```
$  python -m venv venv
```

For Mac

```
$  python3 -m venv venv
```

Activate Virtual Environment

For Windows

```
$  venv\scripts\activate
```

For Mac

```
$  venv\bin\activate
```

**3. Clone this project**

```
$ git clone https://github.com/ShrinidhiYalawar/logregs.git
```

Then, Enter the project

```
$ cd logregs/logregs_project
```

**4. Install Requirements from 'requirements.txt'**

```python
$  pip install -r requirements.txt
```
**5. Now Run Server**

Command for PC:

```python
$ python manage.py runserver
```

Command for Mac:

```python
$ python3 manage.py runserver
```

**6. Login Credentials**

Create Super User (HOD)

```
$  python manage.py createsuperuser
```

Then Add Email, Username and Password

## Copyrights
© 2025 Shrinidhi Yalawar. All rights reserved.


