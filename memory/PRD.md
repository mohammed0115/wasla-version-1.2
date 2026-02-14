# Wasla SaaS Platform - Product Requirements Document

## Original Problem Statement
Build a multi-tenant e-commerce SaaS platform for Saudi & Gulf merchants with:
- Store creation and management
- Product catalog with bulk import
- Order management with exports
- Theme selection and branding
- AI tools (visual search, description generation)
- Arabic RTL support

## Repository
- GitHub: `https://github.com/mohammed0115/wasla-version-1.2`
- Source: User-uploaded `wasla-version-1.2-main.zip`
- Architecture: Clean Architecture (domain / application / infrastructure / interfaces)
- Stack: Django 5.x + DRF + SQLite (MySQL-ready)
- Multi-tenant enforced

---

## Current Status ✅ DEPLOYED

The original Django project has been properly deployed with:
- All Django apps intact
- Database with existing data (db.sqlite3)
- Static files serving via `/api/static/`
- Arabic RTL support working
- Language switching functional

---

## Project Structure
```
/app/backend/
├── accounts/          # User authentication
├── ai/                # AI tools (visual search, description)
├── analytics/         # Event tracking, experiments
├── cart/              # Shopping cart
├── catalog/           # Products, categories
├── checkout/          # Checkout flow
├── config/            # Django settings, URLs
├── customers/         # Customer management
├── domains/           # Custom domain support
├── emails/            # Email service
├── exports/           # CSV/PDF exports
├── imports/           # Bulk product import
├── locale/            # ar/en translations
├── notifications/     # Push notifications
├── observability/     # Logging, metrics
├── orders/            # Order management
├── payments/          # Payment processing
├── plugins/           # Plugin system
├── reviews/           # Product reviews
├── security/          # Security middleware
├── settlements/       # Merchant settlements
├── shipping/          # Shipping providers
├── sms/               # SMS service
├── static/            # CSS, JS, images
├── stores/            # Store management
├── subscriptions/     # Subscription plans
├── system/            # System config
├── templates/         # HTML templates
├── tenants/           # Multi-tenancy
├── themes/            # Theme selection
├── wallet/            # Wallet/credits
├── webhooks/          # Webhook handling
├── db.sqlite3         # SQLite database
├── manage.py          # Django CLI
└── requirements.txt   # Python dependencies
```

---

## Environment Configuration

### .env
```
SECRET_KEY=django-insecure-change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,*.preview.emergentagent.com,*.preview.emergentcf.cloud

CSRF_TRUSTED_ORIGINS=https://*.preview.emergentagent.com,https://*.preview.emergentcf.cloud

DEFAULT_FROM_EMAIL=Wasla <info@w-sala.com>
SERVER_EMAIL=info@w-sala.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@w-sala.com
EMAIL_HOST_PASSWORD=YazYaz@2030
```

### Static Files
- STATIC_URL: `/api/static/`
- MEDIA_URL: `/api/media/`
- Required for platform ingress routing

---

## URL Structure

### Web Pages (via /api/ prefix for ingress)
- `/api/` - Home page
- `/api/auth/` - Authentication
- `/api/dashboard/` - Merchant dashboard
- `/api/dashboard/setup` - Store setup wizard
- `/api/dashboard/import` - Bulk import
- `/api/dashboard/exports` - Order exports
- `/api/dashboard/themes` - Theme selection

### REST APIs
- `/api/v1/ai/` - AI endpoints
- `/api/v1/analytics/` - Analytics
- `/api/v1/cart/` - Cart
- `/api/v1/checkout/` - Checkout
- `/api/v1/orders/` - Orders

---

## Pending Tasks

### Sprint 1 (Production Hardening)
- [ ] Celery + Redis integration
- [ ] Upload security hardening
- [ ] Production settings
- [ ] Health endpoints

### Phase 0 (Stabilization)
- [ ] i18n/RTL verification
- [ ] CSS conflict resolution
- [ ] Auth guards audit

### Phase 3 (Features)
- [ ] Merchant Dashboard KPIs
- [ ] Order export improvements
- [ ] Bulk import UI
- [ ] Theme selection

---

## Testing Credentials
- **Email:** `merchant@test.com`
- **Password:** `password`

---

## Changelog

### Feb 14, 2026
- Restored original Django project from user-uploaded zip
- Fixed static file serving with /api/ prefix
- Updated ALLOWED_HOSTS for preview environment
- Configured CSRF_TRUSTED_ORIGINS
