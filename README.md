# Quiz Portal Web Application

## Overview
This project is a **quiz management web application** that allows users to register, attempt quizzes, and track their performance.  
Administrators can create and manage subjects, chapters, and quizzes. The system provides performance analytics, attempt histories, and summary reports.  

The application is built using **Flask** and follows the **Model-View-Controller (MVC)** architecture pattern with **Jinja2** templates for the front-end.

---

## Technologies Used

| Technology | Purpose |
|-------------|----------|
| **Flask** | Backend framework used for routing, authentication, and business logic. |
| **Jinja2** | Template engine for rendering dynamic web pages. |
| **SQLite** | Lightweight relational database used for local storage. |
| **SQLAlchemy** | ORM for defining and managing database models and relationships. |
| **Bootstrap** | Provides responsive front-end layout and styling. |

---

## Database Design

### User
| Field | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `username` | STRING | UNIQUE, NOT NULL |
| `password` | STRING | NOT NULL |
| `fullname` | STRING | NOT NULL |
| `qualification` | STRING | Optional |
| `dob` | STRING | Optional |

### Subject
| Field | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `name` | STRING | NOT NULL |
| `description` | STRING | Optional |

### Chapter
| Field | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `subject_id` | INTEGER | NOT NULL, FOREIGN KEY → Subject(id) ON DELETE CASCADE |
| `name` | STRING | NOT NULL |
| `description` | STRING | Optional |

### Quiz
| Field | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `name` | STRING | NOT NULL |
| `chapter_id` | INTEGER | NOT NULL, FOREIGN KEY → Chapter(id) ON DELETE CASCADE |
| `remarks` | STRING | Optional |

### Question
| Field | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `quiz_id` | INTEGER | NOT NULL, FOREIGN KEY → Quiz(id) ON DELETE CASCADE |
| `statement` | STRING | NOT NULL |
| `option_1` | STRING | NOT NULL |
| `option_2` | STRING | NOT NULL |
| `option_3` | STRING | NOT NULL |
| `option_4` | STRING | NOT NULL |
| `correct_answer` | STRING | NOT NULL |

### Score
| Field | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY → User(id) ON DELETE CASCADE |
| `quiz_id` | INTEGER | NOT NULL, FOREIGN KEY → Quiz(id) ON DELETE CASCADE |
| `time_stamp_of_attempt` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `total_scored` | INTEGER | NOT NULL |
| `total_question` | INTEGER | NOT NULL |

---

## Architecture
The project is organized using the **MVC (Model-View-Controller)** pattern:

- **Models (`models.py`)**: Defines database schema and relationships using SQLAlchemy.  
- **Controllers (Flask routes)**: Handle user interactions, quiz logic, and authentication.  
- **Views (`templates/`)**: HTML templates rendered using Jinja2 for dynamic content.  

---

## Features
- Secure user authentication and session handling  
- Admin dashboard for managing subjects, chapters, and quizzes  
- Quiz participation with instant scoring feedback  
- Detailed analytics and performance summaries  
- Relational database structure with cascading deletes  
- Responsive web design using Bootstrap  
- Extensible modular architecture  

**Clone the repository**
   ```bash
   git clone https://github.com/akrutipagar/Quiz_Master_App.git
   cd Quiz_Master_App

