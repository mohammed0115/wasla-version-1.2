# Wasla E-commerce Platform - Phase 3 PRD

## Original Problem Statement
Implement Phase 3 ONLY: "MERCHANT GROWTH & STORE SETUP AUTOMATION" for existing Django 5 e-commerce platform.

## Architecture
- **Framework**: Django 5 with Clean Architecture (domain/application/infrastructure/interfaces)
- **Frontend**: Django Templates + Bootstrap RTL
- **API**: Django REST Framework
- **Database**: SQLite (MySQL-compatible design)
- **Multi-tenant**: Enforced via `store_id` on all queries

## User Personas
- **Merchant**: Creates stores, uploads products, manages orders, customizes branding
- **Customer**: Browses products, places orders, tracks deliveries

## Core Requirements (Phase 3 P1)

### 1. Bulk Product Upload (CSV + Images) ✅
- CSV template download with Arabic/English headers
- Drag-and-drop upload zone for CSV (max 5MB)
- Multi-image upload (up to 50 images, jpg/png/webp, max 5MB each)
- Validation: headers, required fields, SKU uniqueness, number formats
- Progress tracking and error display
- Import job history

### 2. Theme Selection + Branding ✅
- 5 pre-built themes: classic, modern, minimal, elegant, bold
- Live preview of theme selection
- Full branding customization:
  - Logo upload (PNG/JPG)
  - Primary, secondary, accent colors (#RRGGBB validation)
  - Font family selection (Tajawal, Cairo, Noto Sans Arabic, Inter, Almarai)
- Real-time preview panel

### 3. Order Exports (CSV + PDF Invoice) ✅
- Orders CSV export with filters (status, date range)
- Professional PDF invoice generation with:
  - Header with branding colors
  - Customer info and order details
  - Line items with pricing
  - VAT calculation (15%)
  - Total amount

### 4. Setup Wizard UX Improvements ✅
- Enhanced UI with progress indicators
- Better form validation feedback
- Streamlined 4-step wizard flow

## What's Been Implemented (2026-02-14)

### Files Created/Modified

#### Import Module
- `/app/wasla_repo/imports/interfaces/web/views.py` - Added CSV template download
- `/app/wasla_repo/imports/interfaces/web/urls.py` - Added template route
- `/app/wasla_repo/templates/dashboard/import/index.html` - Rich drag-drop UI
- `/app/wasla_repo/templates/dashboard/import/job_detail.html` - Enhanced status page

#### Themes Module
- `/app/wasla_repo/themes/interfaces/web/views.py` - Added font choices, fixed redirects
- `/app/wasla_repo/themes/migrations/0004_add_more_themes.py` - Added elegant, bold themes
- `/app/wasla_repo/templates/dashboard/themes/list.html` - Theme grid with previews
- `/app/wasla_repo/templates/dashboard/branding/edit.html` - Full branding editor

#### Exports Module
- `/app/wasla_repo/exports/interfaces/web/views.py` - Added orders list context
- `/app/wasla_repo/exports/interfaces/web/urls.py` - Fixed URL names
- `/app/wasla_repo/exports/infrastructure/exporters.py` - Enhanced PDF invoice
- `/app/wasla_repo/templates/dashboard/exports/index.html` - Rich export UI

### Database Seed Data
- Test user: merchant@test.com / test1234
- Test tenant: test-store (متجر اختبار)
- 5 themes seeded
- Sample products and orders

## Prioritized Backlog

### P0 (Critical) - DONE
- ✅ Bulk CSV upload with validation
- ✅ Theme selection UI
- ✅ Basic branding customization
- ✅ Order CSV export
- ✅ PDF invoice generation

### P1 (High Priority)
- Background job processing for large imports (Celery)
- Bulk invoice PDF generation
- Image URL support in CSV import

### P2 (Medium Priority)
- Theme preview images
- Advanced color palette extraction from logo
- Export job history

### P3 (Low Priority)
- Full theme marketplace
- Custom theme creation
- RTL PDF with Arabic fonts

## Next Tasks
1. Test authentication flow with actual browser session
2. Add background job support for large imports
3. Implement image URL download during import
4. Add bulk invoice generation feature

## Technical Notes
- Dashboard pages require authentication and tenant context
- CSV template endpoint is public (no auth required)
- All queries filtered by store_id for tenant isolation
- Colors validated to #RRGGBB format only
