# Wasla E-commerce Platform - Phase 3 PRD

## Original Problem Statement
Implement Phase 3 ONLY: "MERCHANT GROWTH & STORE SETUP AUTOMATION" for existing Django 5 e-commerce platform + Unified Merchant Dashboard UI following PROTOTYPE_SCENARIOS.pdf.

## Architecture
- **Framework**: Django 5 with Clean Architecture (domain/application/infrastructure/interfaces)
- **Frontend**: Django Templates + Bootstrap RTL
- **API**: Django REST Framework
- **Database**: SQLite (MySQL-compatible design)
- **Multi-tenant**: Enforced via `store_id` on all queries

## User Personas
- **Merchant**: Creates stores, uploads products, manages orders, customizes branding
- **Customer**: Browses products, places orders, tracks deliveries

## Core Requirements

### Phase 3 P1: Merchant Growth & Store Setup Automation
1. ✅ Bulk Product Upload (CSV + Images)
2. ✅ Theme Selection + Branding Improvements
3. ✅ Order Exports (CSV + PDF Invoice)
4. ✅ Setup Wizard UX Improvements

### Unified Merchant Dashboard UI
1. ✅ Dashboard Overview with KPI cards
2. ✅ Orders List with status chips
3. ✅ Products List
4. ✅ Settlements with balance summary
5. ✅ AI Tools integration
6. ✅ Store Settings form
7. ✅ RTL/LTR language switching

## Scenario → Screen Map

| Screen | URL | Template | View |
|--------|-----|----------|------|
| Dashboard Overview | /dashboard/overview | dashboard/overview.html | dashboard_overview |
| Orders List | /dashboard/orders | dashboard/orders/list.html | dashboard_orders |
| Products List | /dashboard/products | dashboard/products/list.html | dashboard_products |
| Settlements | /dashboard/settlements | dashboard/settlements/list.html | settlement_list |
| AI Tools | /dashboard/ai/tools | dashboard/ai/tools.html | ai_tools |
| Store Settings | /dashboard/store/info | dashboard/store/settings.html | store_settings_update |
| Themes | /dashboard/themes | dashboard/themes/list.html | themes_list |
| Branding | /dashboard/branding | dashboard/branding/edit.html | branding_edit |
| Imports | /dashboard/import | dashboard/import/index.html | import_index |
| Exports | /dashboard/exports | dashboard/exports/index.html | exports_index |

## What's Been Implemented (2026-02-14)

### Dashboard Framework
- `templates/dashboard/base_dashboard.html` - Main dashboard shell
- `templates/dashboard/partials/sidebar.html` - Sidebar navigation
- `templates/dashboard/partials/topbar.html` - Top bar with language switcher
- `static/css/dashboard.css` - Unified dashboard styling

### New Views Added
- `tenants/interfaces/web/views.py`:
  - `dashboard_overview()` - KPI cards, recent orders
  - `dashboard_orders()` - Orders list
  - `dashboard_products()` - Products list

### Authentication Guards
- All dashboard views decorated with `@login_required`
- All tenant-specific views decorated with `@tenant_access_required`
- Unauthenticated users redirect to `/auth/?next=...`

### Design Tokens Used (from existing app.css)
- `--bg:#ffffff`, `--text:#0f172a`, `--muted:#64748b`
- `--line:#e5e7eb`, `--card:#ffffff`, `--soft:#f6f8fb`
- `--input:#eaf2ff`, `--primary:#1F4FD8`, `--danger:#ef4444`
- `--shadow:0 10px 30px rgba(15,23,42,.08)`, `--radius:14px`

### Files Created/Modified

#### New Files
- `/app/wasla_repo/templates/dashboard/base_dashboard.html`
- `/app/wasla_repo/templates/dashboard/partials/sidebar.html`
- `/app/wasla_repo/templates/dashboard/partials/topbar.html`
- `/app/wasla_repo/templates/dashboard/overview.html`
- `/app/wasla_repo/templates/dashboard/orders/list.html`
- `/app/wasla_repo/templates/dashboard/products/list.html`
- `/app/wasla_repo/templates/dashboard/store/settings.html`
- `/app/wasla_repo/static/css/dashboard.css`

#### Modified Files
- `/app/wasla_repo/tenants/urls.py` - Added dashboard routes
- `/app/wasla_repo/tenants/interfaces/web/views.py` - Added dashboard views
- `/app/wasla_repo/ai/interfaces/web/views.py` - Added @login_required
- `/app/wasla_repo/exports/interfaces/web/views.py` - Added @login_required
- `/app/wasla_repo/settlements/interfaces/web/views.py` - Added @login_required
- `/app/wasla_repo/accounts/views.py` - Fixed login redirect to dashboard

### Test Data Seeded
- User: merchant@test.com / test1234
- Store: test-store with products and orders

## Manual QA Checklist
- [x] Login redirect works (/auth/?next=...)
- [x] /dashboard/ loads (redirects to overview)
- [x] RTL/LTR flips layout correctly
- [x] Language switch affects ALL content
- [x] Mobile responsiveness (sidebar collapses)
- [x] No NoReverseMatch errors
- [x] No 405 method errors
- [x] No AnonymousUser TypeError

## Next Action Items
- P1: Fix frontend login form tab switching UI issue
- P2: Add Celery background jobs for large imports
- P2: Implement analytics data for KPI cards

## Technical Notes
- Dashboard pages require authentication via @login_required
- Tenant context required via @tenant_access_required
- All queries filtered by store_id for tenant isolation
- Language switching uses Django's set_language view
