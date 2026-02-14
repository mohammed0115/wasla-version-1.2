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
- Architecture: Clean Architecture (domain / application / infrastructure / interfaces)
- Stack: Django 5.x + DRF + SQLite (MySQL-ready)
- Multi-tenant enforced

---

## Sprint 1 - Production Hardening ✅ COMPLETED

### Celery + Redis Integration
- Proper Celery app with auto-discovery
- Environment-based broker configuration
- JSON serialization only
- Exponential backoff retry logic
- Task routing to specialized queues

### Upload Security Hardening
- File size limit (5MB max)
- MIME type validation
- Double-extension attack prevention
- Path traversal prevention
- Filename sanitization

### Production Settings
- Security headers enabled
- CSRF/HTTPS settings
- Structured JSON logging
- Startup validation

### Health & Observability
- `/api/healthz` - Liveness probe
- `/api/readyz` - Readiness probe
- `/api/health` - Comprehensive status

---

## Phase 0 - Stabilization ✅ COMPLETED (Feb 14, 2026)

### 1. i18n / RTL Fix ✅
- `base.html` uses `LANGUAGE_BIDI` for `dir` attribute
- LocaleMiddleware enabled and correctly ordered
- Language switch uses Django `set_language` POST
- All templates use `{% trans %}` tags
- RTL CSS loads conditionally via `LANGUAGE_BIDI`
- Arabic translations compiled and working

**Verification:**
- ✅ Language switching reloads page fully translated
- ✅ No English inside Arabic mode
- ✅ No Arabic inside English mode
- ✅ Layout direction changes correctly

### 2. CSS Conflict Resolution ✅
- Consolidated CSS into single `static/css/app.css`
- Single `:root` declaration
- No duplicate class definitions
- RTL/LTR overrides in separate files
- Bootstrap RTL conflicts resolved

**Verification:**
- ✅ No duplicated CSS classes
- ✅ No visual breaks in RTL
- ✅ No override conflicts

### 3. Authentication & Tenant Guards ✅
- `LOGIN_URL` configured in settings
- All dashboard views use `@login_required`
- All tenant views use `@tenant_access_required`
- Proper decorator ordering (login_required -> tenant_access_required)

**Files Updated:**
- `analytics/interfaces/web/views.py` - Added `@login_required`
- `exports/interfaces/web/views.py` - Added `@login_required`
- `imports/interfaces/web/views.py` - Added `@login_required`
- `ai/interfaces/web/views.py` - Fixed decorator ordering
- `themes/interfaces/web/views.py` - Added `@login_required`

**Verification:**
- ✅ Anonymous users cannot access dashboard
- ✅ User cannot access another tenant
- ✅ No security holes

---

## Phase 3 - Feature Implementation ✅ COMPLETED (Feb 14, 2026)

### 1. Merchant Dashboard ✅
**File:** `tenants/interfaces/web/dashboard_views.py`
**Template:** `templates/dashboard/merchant/home.html`

**KPIs Implemented:**
- Orders Today
- Orders (Last 7 Days)
- Revenue Today
- Revenue (Last 30 Days)
- Average Order Value
- Paid vs Pending Orders

**Widgets:**
- Recent Orders table (last 10)
- Top Products (last 7 days)
- Quick Actions panel
- Store Stats

**Query Optimizations:**
- Single aggregated queries for KPIs
- `select_related` for recent orders
- `values().annotate()` for top products
- No N+1 queries

### 2. Order Export System ✅
**Template:** `templates/dashboard/exports/index.html`

**Features:**
- CSV export with date range filter
- Status filtering
- PDF invoice download (per order)
- Arabic RTL support in PDF

### 3. Theme Selection & Branding ✅
Already implemented in previous sprint

### 4. Bulk Import UI Improvements ✅
**Template:** `templates/dashboard/import/index.html`

**Features:**
- Drag-drop style file upload
- Visual file selection feedback
- Progress indicator during upload
- Recent import jobs list
- Error display in job details

---

## Key Files Structure
```
/app/backend/
├── config/
│   ├── celery.py            # Celery configuration
│   ├── settings.py          # Production settings
│   └── urls.py              # URL routing with /api/ prefix
├── static/css/
│   ├── app.css              # Main consolidated CSS
│   ├── rtl.css              # RTL overrides
│   └── ltr.css              # LTR overrides
├── locale/
│   ├── ar/LC_MESSAGES/      # Arabic translations
│   └── en/LC_MESSAGES/      # English translations
├── tenants/interfaces/web/
│   ├── dashboard_views.py   # Merchant dashboard
│   └── decorators.py        # Auth guards
├── templates/dashboard/
│   ├── merchant/home.html   # Dashboard template
│   ├── exports/index.html   # Export page
│   └── import/index.html    # Import page
└── security/
    └── upload_validator.py  # Upload security
```

---

## API Endpoints

### Health
- `GET /api/healthz` - Liveness
- `GET /api/readyz` - Readiness
- `GET /api/health` - Full status

### Dashboard
- `GET /api/dashboard/` - Merchant dashboard
- `GET /api/dashboard/home` - Merchant dashboard (alias)

### Exports
- `GET /api/dashboard/exports` - Export page
- `GET /api/dashboard/exports/csv` - CSV download
- `GET /api/dashboard/exports/invoice/<order_id>` - PDF invoice

### Imports
- `GET /api/dashboard/import` - Import page
- `POST /api/dashboard/import/start` - Start import
- `GET /api/dashboard/import/<job_id>` - Job details

---

## Environment Variables
See `.env.production.example` for full list

---

## Testing Credentials
- **Email:** `merchant@test.com`
- **Password:** `password`

---

## Next Steps (Backlog)

### P1 - High Priority
- [ ] Redis deployment for production Celery
- [ ] MySQL migration
- [ ] Payment integration (Stripe/PayPal)

### P2 - Medium Priority
- [ ] Product CRUD UI improvements
- [ ] Customer management
- [ ] Shipping providers integration

### P3 - Low Priority
- [ ] Prometheus metrics
- [ ] Rate limiting middleware
- [ ] Advanced analytics dashboard

---

## Changelog

### Feb 14, 2026
- Sprint 1: Production hardening completed
- Phase 0: Stabilization completed (i18n, CSS, auth guards)
- Phase 3: Feature implementation completed (dashboard, exports, imports)
