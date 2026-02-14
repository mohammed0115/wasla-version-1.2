# Wasla SaaS Platform - Product Requirements Document

## Original Problem Statement
Transform the Wasla Django SaaS e-commerce platform from MVP into production-ready infrastructure with:
1. Celery + Redis async task processing
2. Upload security hardening
3. Production settings hardening
4. Health & observability endpoints
5. Code quality enforcement

## Repository
- GitHub: `https://github.com/mohammed0115/wasla-version-1.2`
- Architecture: Clean Architecture (domain / application / infrastructure / interfaces)
- Stack: Django 5.x + DRF + SQLite (MySQL-ready)
- Multi-tenant enforced

## Sprint 1 Implementation Status

### ✅ COMPLETED

#### Part 1 - Celery + Redis (Production Grade)
- [x] `config/celery.py` - Proper Celery app with auto-discovery
- [x] `config/celery_config.py` - Centralized config module
- [x] Environment-based broker & backend configuration
- [x] JSON serialization only
- [x] Timezone consistency with Django
- [x] Task routing to specialized queues (imports, ai, analytics, emails)
- [x] `ai/tasks.py` - AI indexing tasks with retries
- [x] `imports/tasks.py` - Bulk import async tasks
- [x] `analytics/tasks.py` - KPI aggregation tasks
- [x] Exponential backoff retry logic (3 retries max)
- [x] Task timeouts (soft: 5min, hard: 10min)
- [x] Structured JSON task logging
- [x] Eager mode fallback for dev without Redis

#### Part 2 - Upload Security Hardening
- [x] `security/upload_validator.py` - Comprehensive validation
- [x] File size limit (5MB max)
- [x] MIME type validation (python-magic + Pillow fallback)
- [x] Extension whitelist enforcement
- [x] Double-extension attack prevention
- [x] Path traversal prevention
- [x] Actual image content validation
- [x] Filename sanitization with UUID
- [x] Integrated into imports views

#### Part 3 - Production Settings Hardening
- [x] `config/settings.py` - Full production rewrite
- [x] SECRET_KEY from environment
- [x] DEBUG = False enforcement
- [x] ALLOWED_HOSTS validation
- [x] CSRF_TRUSTED_ORIGINS configured
- [x] SecurityMiddleware enabled
- [x] SECURE_CONTENT_TYPE_NOSNIFF = True
- [x] SECURE_BROWSER_XSS_FILTER = True
- [x] X_FRAME_OPTIONS = "DENY"
- [x] SESSION_COOKIE_SECURE (env toggle)
- [x] CSRF_COOKIE_SECURE (env toggle)
- [x] Production validation at startup
- [x] `.env.production.example` template

#### Part 4 - Health & Observability
- [x] `observability/views/health.py` - Production-grade checks
- [x] `/healthz` - Liveness probe (fast)
- [x] `/readyz` - Readiness probe (all deps)
- [x] `/health` - Comprehensive status
- [x] Database connectivity check
- [x] Redis connectivity check
- [x] Celery worker availability check
- [x] Django cache check
- [x] Structured JSON response with latencies
- [x] Request timing middleware
- [x] X-Request-Id header propagation

#### Part 5 - Code Quality
- [x] Clean separation of concerns maintained
- [x] No business logic in views
- [x] Dependency inversion via use cases
- [x] Idempotent task design
- [x] Proper error handling

#### Part 6 - Logging Configuration
- [x] Structured JSON logging
- [x] Separate handlers: app, celery, errors
- [x] Rotating file handlers (10MB, 5 backups)
- [x] Mail admins on errors (production)
- [x] Request context enrichment

### Platform Integration
- [x] Supervisor config updated for Gunicorn
- [x] URL routing supports `/api/` prefix
- [x] ALLOWED_HOSTS includes preview domains

## Key Files
```
/app/backend/
├── config/
│   ├── __init__.py       # Celery app loader
│   ├── celery.py         # Celery configuration
│   ├── celery_config.py  # Centralized settings
│   ├── settings.py       # Production-hardened
│   └── urls.py           # Health endpoints
├── security/
│   ├── upload_validator.py    # Upload security
│   └── production_settings.py # Settings helpers
├── ai/
│   └── tasks.py          # AI async tasks
├── imports/
│   └── tasks.py          # Import async tasks
├── analytics/
│   ├── models.py         # DailyKPI model added
│   └── tasks.py          # KPI async tasks
├── observability/
│   └── views/health.py   # Health endpoints
├── .env                  # Development config
├── .env.production.example # Production template
└── requirements.txt      # Updated deps
```

## Worker Commands
```bash
# Start Celery worker (production)
celery -A config worker -l INFO -Q default,imports,ai,analytics,emails

# Start Celery beat (scheduled tasks)
celery -A config beat -l INFO

# Run all workers with concurrency
celery -A config worker -l INFO -c 4 -Q default,imports,ai,analytics,emails
```

## API Endpoints
- `GET /api/healthz` - Liveness (always 200)
- `GET /api/readyz` - Readiness (200 or 503)
- `GET /api/health` - Full status JSON

## Environment Variables
See `.env.production.example` for full list

## Next Steps (P1)
1. Phase 0 Stabilization
   - CSS conflicts consolidation
   - i18n/RTL fixes
   - Auth guards verification
2. Phase 3 Features
   - Bulk product upload (UI)
   - Theme selection & branding
   - Order exports (CSV + PDF)
   - Unified Merchant Dashboard

## Testing Status
- Health endpoints: ✅ Working
- Celery tasks: ✅ Eager mode working
- Upload validation: ✅ Code complete
- Django app: ✅ Running on Gunicorn

## Notes
- Redis not available in preview environment; tasks run in eager mode
- MySQL requires mysqlclient system dependencies; using SQLite
- Preview URL requires `/api/` prefix for all routes
