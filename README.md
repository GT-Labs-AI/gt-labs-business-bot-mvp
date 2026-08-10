\# 🏢 GT Labs Business Bot (Showcase MVP)



\[!\[Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

\[!\[aiogram 3.x](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://docs.aiogram.dev/)

\[!\[SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)



An asynchronous, production-quality Telegram booking bot developed by \*\*\[GT Labs AI](https://github.com/GT-Labs-AI)\*\*. Designed as a showcase MVP for appointment-based service businesses (salons, clinics, consultancies).



\---



\## 🎯 Problem



Small service businesses frequently lose prospective clients due to:

\- Manual, slow client intake processes over messengers.

\- Lack of immediate automated confirmation and validation.

\- Unstructured lead data leading to lost contact records and missing analytics.



\## 💡 Solution



\*\*GT Labs Business Bot\*\* automates client acquisition and appointment scheduling:

1\. Guides clients through an interactive multi-step \*\*Finite State Machine (FSM)\*\* booking workflow.

2\. Validates client inputs (phone numbers, contact payloads) before persisting to the database.

3\. Instantly notifies administrators via Telegram upon confirmed bookings.

4\. Provides real-time operational analytics (`/stats`) and order history (`/orders`) protected by Role-Based Access Control (RBAC).



\---



\## ✨ Key Features



\- \*\*Interactive Navigation:\*\* Main menu with services, pricing, company info, and contacts.

\- \*\*Robust FSM Booking:\*\*

&#x20; - Name input validation.

&#x20; - Native contact-share button or international phone number regex validation.

&#x20; - Interactive Inline Keyboard service selection.

&#x20; - Order summary screen with \*\*Confirm / Cancel\*\* actions.

\- \*\*Administrator Control Panel:\*\*

&#x20; - `/orders`: Displays recent bookings with client details.

&#x20; - `/stats`: Provides aggregated booking metrics (Total, Today, Last 7 Days).

\- \*\*Security \& Integrity:\*\*

&#x20; - Authorization enforced strictly by numeric Telegram User IDs (`ADMIN\_ID`).

&#x20; - Automatic HTML entity escaping (`html.quote`) to prevent Markdown/HTML injection attacks.

&#x20; - Environment-isolated secrets via `pydantic-settings`.



\---



\## 🏗 Architecture \& Design Patterns



The project follows clean architecture principles with strict separation of concerns:



```

Telegram Event -> Middleware (DB Session Injection) -> Handler -> Service Layer -> SQLAlchemy ORM -> SQLite Database

```



\- \*\*Middleware DI:\*\* `DbSessionMiddleware` injects an isolated async SQLAlchemy session per incoming update and handles session cleanup automatically.

\- \*\*Service Layer Pattern:\*\* `UserService` and `AppointmentService` encapsulate all SQL queries and business logic, keeping Telegram handlers lean and testable.

\- \*\*Async Stack:\*\* Built ground-up on Python 3.12 `asyncio`, `aiogram 3`, and `SQLAlchemy 2.0` with `aiosqlite`.



\---



\## 🛠 Tech Stack



| Component | Technology |

| :--- | :--- |

| \*\*Language\*\* | Python 3.12 |

| \*\*Bot Framework\*\* | `aiogram` 3.x (Asyncio Telegram Bot API) |

| \*\*ORM / Database\*\* | `SQLAlchemy` 2.0 + `aiosqlite` (SQLite) |

| \*\*Configuration\*\* | `pydantic-settings` + `python-dotenv` |

| \*\*FSM Storage\*\* | `MemoryStorage` (Development) / `Redis` (Production-ready) |



\---



\## 📁 Project Structure



```text

telegram-bot-template/

├── config/

│   └── config.py              # Pydantic Settings configuration loader

├── app/

│   ├── database/

│   │   ├── connection.py      # Async Engine \& Sessionmaker

│   │   └── models.py          # SQLAlchemy ORM models (User, Appointment)

│   ├── handlers/

│   │   ├── admin.py           # Admin commands (/orders, /stats)

│   │   ├── appointment.py     # Booking FSM flow handlers

│   │   └── common.py          # /start \& informational handlers

│   ├── keyboards/

│   │   ├── inline.py         # Dynamic Inline keyboards

│   │   └── reply.py          # Reply navigation keyboards

│   ├── middlewares/

│   │   └── db.py              # Async DB session injection middleware

│   ├── services/

│   │   ├── appointment\_service.py # Appointment business logic \& stats

│   │   └── user\_service.py    # User registration logic

│   ├── states/

│   │   └── appointment.py     # Aiogram FSM StatesGroup

│   └── utils/

│       ├── logger.py          # Standardized logging setup

│       └── validators.py      # Regex phone number validation

├── main.py                    # Application entry point

├── .env.example               # Environment variables template

├── requirements.txt           # Python dependencies

└── README.md                  # Project documentation

```



\---



\## 🚀 Installation \& Setup



\### Prerequisites



\- Python 3.12+

\- Telegram Bot Token (obtained from \[@BotFather](https://t.me/BotFather))



\### 1. Clone the repository



```bash

git clone https://github.com/GT-Labs-AI/gt-labs-business-bot.git

cd gt-labs-business-bot

```



\### 2. Create and activate a virtual environment



```bash

python3.12 -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install --upgrade pip

pip install -r requirements.txt

```



\### 4. Configure environment variables



Copy `.env.example` to `.env` and fill in your credentials:



```bash

cp .env.example .env

```



Edit `.env`:



```env

BOT\_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ

ADMIN\_ID=987654321

DB\_URL=sqlite+aiosqlite:///gt\_beauty.db

```



\### 5. Run the bot



```bash

python main.py

```



\---



\## 🔒 Security Measures



1\. \*\*Role-Based Access Control:\*\* Admin endpoints use explicit numeric User ID checks (`message.from\_user.id == config.ADMIN\_ID`). Telegram usernames are ignored for auth due to spoofing risks.

2\. \*\*Injection Defense:\*\* All user inputs rendered in Telegram messages pass through `html.quote()` to eliminate HTML/formatting injection.

3\. \*\*Secret Isolation:\*\* API tokens and database URIs are loaded exclusively via environment variables and excluded from version control via `.gitignore`.



\---



\## 🔮 Future Improvements



\- \[ ] Add PostgreSQL database support via `asyncpg`.

\- \[ ] Integrate Redis (`RedisStorage`) for persistent FSM storage across deployments.

\- \[ ] Implement Google Calendar API synchronization for automatic calendar slot locking.

\- \[ ] Add multi-language support (i18n).



\---



\## 📄 License



Distributed under the MIT License. Developed with ❤️ by \*\*\[GT Labs AI](https://github.com/GT-Labs-AI)\*\*.

