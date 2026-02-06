# Donation API

A Django REST Framework–based backend for a donation platform with user management, donation campaigns, and Stripe payment integration.

This project provides comprehensive APIs for managing user accounts, donation campaigns, and processing payments. It is containerized with Docker and designed to run locally and in production on Render.

---

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Payment Integration](#payment-integration)
- [Development](#development)
- [Deployment](#deployment)

---

## 🛠️ Tech Stack

- **Language**: Python 3.14
- **Framework**: Django 6.x
- **REST API**: Django REST Framework
- **Database**: PostgreSQL 18.1
- **Web Server**: Gunicorn
- **Container**: Docker & Docker Compose
- **Payment Processing**: Stripe
- **Image Processing**: Pillow
- **Authentication**: Django REST Framework SimpleJWT
- **Dependency Management**: Poetry

---

## 📁 Project Structure

```
donation-api/
├── accounts/              # User account management
│   ├── models.py         # User-related models
│   ├── views.py          # Account endpoints
│   ├── serializers.py    # Data serialization
│   ├── urls.py           # URL routing
│   └── migrations/       # Database migrations
│
├── donations/            # Donation campaigns
│   ├── models.py         # Donation & Category models
│   ├── views.py          # Donation endpoints
│   ├── serializers.py    # Data serialization
│   ├── signals.py        # Django signals
│   ├── urls.py           # URL routing
│   └── migrations/       # Database migrations
│
├── payments/             # Payment processing
│   ├── models.py         # Payment models
│   ├── views.py          # Payment endpoints
│   ├── serializers.py    # Data serialization
│   ├── stripe_client.py  # Stripe integration
│   ├── webhooks.py       # Stripe webhooks
│   ├── urls.py           # URL routing
│   └── migrations/       # Database migrations
│
├── config/               # Project configuration
│   ├── settings.py       # Settings loader
│   ├── settings/
│   │   ├── base.py      # Base settings
│   │   ├── dev.py       # Development settings
│   │   └── prod.py      # Production settings
│   ├── urls.py          # Root URL configuration
│   ├── wsgi.py          # WSGI application
│   ├── asgi.py          # ASGI application
│   └── health.py        # Health check endpoint
│
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Local development setup
├── entrypoint.sh        # Container entrypoint
├── manage.py            # Django management script
├── pyproject.toml       # Poetry dependency configuration
└── README.md            # This file
```

---

## 📋 Prerequisites

- **Docker** (v20.10+)
- **Docker Compose** (v2.0+)
- Or for local development without Docker:
  - Python 3.14+
  - PostgreSQL 18+
  - Poetry (for dependency management)

---

## ⚙️ Installation & Setup

### Using Docker (Recommended)

1. **Clone the repository**

```bash
git clone <repository-url>
cd donation-api
```

2. **Copy environment file**

```bash
cp .env.example .env.dev
```

3. **Configure environment variables** (see [Environment Variables](#environment-variables))

```bash
nano .env.dev
```

4. **Build and start services**

```bash
docker compose up --build
```

This will:

- Build the Django application container
- Start the PostgreSQL database
- Run migrations automatically
- Create a superuser (if configured)
- Start the development server on `http://localhost:8000`

### Local Development (Without Docker)

1. **Clone the repository**

```bash
git clone <repository-url>
cd donation-api
```

2. **Create virtual environment**

```bash
python3.14 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install poetry
poetry install
```

4. **Set environment variables**

```bash
cp .env.example .env.dev
export $(cat .env.dev | xargs)
```

5. **Set up PostgreSQL**

```bash
# Make sure PostgreSQL is running
# Create database and user
createdb devdb
createuser devuser
# Set password and permissions
psql -c "ALTER USER devuser WITH PASSWORD 'supersecretpassword';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE devdb TO devuser;"
```

6. **Run migrations**

```bash
python manage.py migrate
```

7. **Create superuser**

```bash
python manage.py createsuperuser
```

8. **Start development server**

```bash
python manage.py runserver
```

---

## 🚀 Running the Application

### Using Docker Compose

```bash
# Build and start all services
docker compose up --build

# Start without rebuilding
docker compose up

# Run in background
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f app

# Stop and remove volumes
docker compose down -v
```

### Local Development

```bash
# With venv activated
python manage.py runserver 0.0.0.0:8000
```

The API will be available at: **http://localhost:8000**

### Health Check

```bash
curl http://localhost:8000/healthz/
```

---

## 🔐 Environment Variables

Create a `.env.dev` file in the root directory with the following variables:

```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=config.settings.dev
RUN_MIGRATIONS=true
RUN_COLLECTSTATIC=false
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_HOST=db                          # Use 'localhost' if running locally
DB_NAME=devdb
DB_USER=devuser
DB_PASSWORD=supersecretpassword

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Key Variables Explained

| Variable                 | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| `DJANGO_SECRET_KEY`      | Secret key for Django (keep it secure!)                |
| `DJANGO_SETTINGS_MODULE` | Which settings module to load (dev/prod)               |
| `RUN_MIGRATIONS`         | Auto-run migrations on container start                 |
| `RUN_COLLECTSTATIC`      | Auto-collect static files on container start           |
| `DB_HOST`                | Database hostname (db for Docker, localhost for local) |
| `STRIPE_SECRET_KEY`      | Your Stripe test/live secret key                       |

---

## 📊 Database

### Models

#### Donations App

- **Category**: Donation categories (e.g., Education, Health, Environment)
- **Donation**: Donation campaigns with title, description, amount, and image

#### Accounts App

- **User**: Extended Django user model for authentication

#### Payments App

- **DonationPayment**: Records of donation payments with Stripe integration

### Running Migrations

```bash
# With Docker
docker compose exec app python manage.py migrate

# Locally
python manage.py migrate

# Create specific migration
python manage.py makemigrations

# Show migration status
python manage.py showmigrations
```

---

## 💳 Payment Integration

### Stripe Setup

1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe Dashboard
3. Add keys to `.env.dev`:
   ```env
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```

### Payment Flow

1. Client requests payment creation
2. API creates Stripe PaymentIntent
3. Client confirms payment with Stripe
4. Webhook updates payment status in database

### Testing Stripe

Use Stripe test cards:

- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **3D Secure**: 4000 0025 0000 3155

---

## 🔨 Development

### Running Tests

```bash
# With Docker
docker compose exec app pytest

# Locally
pytest

# With coverage
pytest --cov=.
```

### Code Formatting & Linting

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Fix linting issues
ruff check --fix .
```

### Pre-commit Hooks

```bash
# Install
pre-commit install

# Run manually
pre-commit run --all-files
```

### Django Admin

Access the Django admin panel at: **http://localhost:8000/admin/**

---

## 🌐 API Endpoints

### Health Check

```
GET /healthz/ - Application health status
```

### Donations

```
GET    /api/v1/categories/                      - List categories with donations
GET    /api/v1/donations/{id}/                  - Retrieve donation
```

### Accounts

```
POST   /api/v1/accounts/auth/register/          - User registration
POST   /api/v1/accounts/auth/login/             - User login
POST   /api/v1/accounts/auth/refresh/           - Refresh Token
POST   /api/v1/accounts/auth/logout/            - User logout
GET    /api/v1/accounts/me/                     - Get user profile
```

### Payments

```
POST   /api/v1/payments/create-payment-intent/  - Create payment intent
GET    /api/v1/payments/my-donations/           - List user payments
GET    /api/v1/payments/stripe-publishable-key/ - Stripe publishable key
POST   /api/v1/payments/webhook/                - Stripe webhook (internal)
```

---

## 📦 Deployment

### Deploying to Render

1. **Push code to GitHub**

```bash
git push origin main
```

2. **Create Render Web Service**
   - Connect your GitHub repository
   - Set Build Command: `poetry install`
   - Set Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:8000`

3. **Configure Environment Variables**
   - Add all variables from `env.example` in Render dashboard

4. **Add PostgreSQL Database**
   - Render will provide `DATABASE_URL`

5. **Deploy**
   - Render will automatically deploy on push

### Production Settings

For production, use `config.settings.prod`:

```env
DJANGO_SETTINGS_MODULE=config.settings.prod
RUN_MIGRATIONS=true
RUN_COLLECTSTATIC=true
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the maintainers.

---

## 🙏 Acknowledgments

- Django and DRF communities
- Stripe for payment processing
- PostgreSQL documentation
