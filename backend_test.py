#!/usr/bin/env python3
"""
Backend API Testing for Wasla Django E-commerce Platform - Phase 3
Tests import, themes, branding, and export functionality
"""

import requests
import sys
import os
import tempfile
import csv
from datetime import datetime
from urllib.parse import urljoin

class WaslaAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.tests_run = 0
        self.tests_passed = 0
        self.csrf_token = None
        
    def get_csrf_token(self):
        """Get CSRF token from login page"""
        try:
            response = self.session.get(f"{self.base_url}/auth/login/")
            if response.status_code == 200:
                # Extract CSRF token from response
                import re
                csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
                    return True
        except Exception as e:
            print(f"Failed to get CSRF token: {e}")
        return False

    def login(self, username="merchant", password="test1234"):
        """Login to get authenticated session"""
        print(f"\n🔐 Logging in as {username}...")
        
        if not self.get_csrf_token():
            print("❌ Failed to get CSRF token")
            return False
            
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': self.csrf_token
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login/",
                data=login_data,
                headers={'Referer': f"{self.base_url}/auth/login/"}
            )
            
            if response.status_code == 302 or 'dashboard' in response.url:
                print("✅ Login successful")
                return True
            else:
                print(f"❌ Login failed - Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = urljoin(self.base_url, endpoint)
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
                headers['Referer'] = self.base_url
            
            if method == 'GET':
                response = self.session.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    # For file uploads, add CSRF token to data
                    if data is None:
                        data = {}
                    data['csrfmiddlewaretoken'] = self.csrf_token
                    response = self.session.post(url, data=data, files=files, headers={'Referer': self.base_url})
                else:
                    response = self.session.post(url, data=data, headers=headers)
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if response.headers.get('content-type', '').startswith('text/html'):
                    print(f"   Response: HTML page ({len(response.text)} chars)")
                elif response.headers.get('content-type', '').startswith('text/csv'):
                    print(f"   Response: CSV file ({len(response.content)} bytes)")
                elif response.headers.get('content-type', '').startswith('application/pdf'):
                    print(f"   Response: PDF file ({len(response.content)} bytes)")
                else:
                    print(f"   Response: {response.headers.get('content-type', 'unknown')}")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text[:200]}...")
            
            return success, response
            
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, None

    def test_csv_template_download(self):
        """Test CSV template download endpoint"""
        success, response = self.run_test(
            "CSV Template Download",
            "GET", 
            "/dashboard/import/template",
            200
        )
        
        if success and response:
            # Verify it's a CSV file
            content_type = response.headers.get('content-type', '')
            if 'text/csv' in content_type:
                print("   ✅ Correct content type: CSV")
                
                # Check CSV content
                csv_content = response.text
                if 'name_ar,name_en' in csv_content:
                    print("   ✅ CSV headers found")
                else:
                    print("   ⚠️  CSV headers not found")
                    
                # Check for sample data
                if 'قميص أبيض كلاسيكي' in csv_content:
                    print("   ✅ Sample data found")
                else:
                    print("   ⚠️  Sample data not found")
            else:
                print(f"   ❌ Wrong content type: {content_type}")
                
        return success

    def test_import_index_page(self):
        """Test import index page"""
        success, response = self.run_test(
            "Import Index Page",
            "GET",
            "/dashboard/import",
            200
        )
        
        if success and response:
            # Check for key elements in HTML
            html = response.text
            if 'csv-upload-zone' in html:
                print("   ✅ CSV upload zone found")
            if 'images-upload-zone' in html:
                print("   ✅ Images upload zone found")
            if 'download-csv-template' in html:
                print("   ✅ Template download link found")
                
        return success

    def test_themes_list_page(self):
        """Test themes list page"""
        success, response = self.run_test(
            "Themes List Page",
            "GET",
            "/dashboard/themes",
            200
        )
        
        if success and response:
            html = response.text
            themes = ['classic', 'modern', 'minimal', 'elegant', 'bold']
            found_themes = 0
            
            for theme in themes:
                if f'theme-card-{theme}' in html:
                    found_themes += 1
                    print(f"   ✅ Theme {theme} found")
                else:
                    print(f"   ❌ Theme {theme} not found")
                    
            if found_themes == 5:
                print("   ✅ All 5 themes found")
            else:
                print(f"   ⚠️  Only {found_themes}/5 themes found")
                
        return success

    def test_theme_selection(self):
        """Test theme selection form submission"""
        success, response = self.run_test(
            "Theme Selection",
            "POST",
            "/dashboard/themes",
            302,  # Expect redirect after successful form submission
            data={'theme_code': 'modern'}
        )
        return success

    def test_branding_edit_page(self):
        """Test branding edit page"""
        success, response = self.run_test(
            "Branding Edit Page",
            "GET",
            "/dashboard/branding",
            200
        )
        
        if success and response:
            html = response.text
            elements = [
                'primary-color-picker',
                'secondary-color-picker', 
                'accent-color-picker',
                'logo-upload',
                'font-select',
                'live-preview'
            ]
            
            for element in elements:
                if element in html:
                    print(f"   ✅ {element} found")
                else:
                    print(f"   ❌ {element} not found")
                    
        return success

    def test_branding_form_submission(self):
        """Test branding form submission"""
        success, response = self.run_test(
            "Branding Form Submission",
            "POST",
            "/dashboard/branding",
            302,  # Expect redirect after successful form submission
            data={
                'primary_color': '#FF5733',
                'secondary_color': '#33FF57',
                'accent_color': '#3357FF',
                'font_family': 'Cairo'
            }
        )
        return success

    def test_exports_index_page(self):
        """Test exports index page"""
        success, response = self.run_test(
            "Exports Index Page",
            "GET",
            "/dashboard/exports",
            200
        )
        
        if success and response:
            html = response.text
            elements = [
                'orders-csv-export',
                'invoice-pdf-export',
                'export-csv-btn',
                'orders-table'
            ]
            
            for element in elements:
                if element in html:
                    print(f"   ✅ {element} found")
                else:
                    print(f"   ❌ {element} not found")
                    
        return success

    def test_orders_csv_export(self):
        """Test orders CSV export"""
        success, response = self.run_test(
            "Orders CSV Export",
            "GET",
            "/dashboard/exports/orders.csv",
            200
        )
        
        if success and response:
            content_type = response.headers.get('content-type', '')
            if 'text/csv' in content_type:
                print("   ✅ Correct content type: CSV")
            else:
                print(f"   ❌ Wrong content type: {content_type}")
                
        return success

    def test_pdf_invoice_generation(self):
        """Test PDF invoice generation for a sample order"""
        # Try with order ID 1 (should exist based on seeded data)
        success, response = self.run_test(
            "PDF Invoice Generation",
            "GET",
            "/dashboard/exports/invoice/1.pdf",
            200
        )
        
        if success and response:
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                print("   ✅ Correct content type: PDF")
                if len(response.content) > 1000:  # PDF should be substantial
                    print(f"   ✅ PDF size looks good: {len(response.content)} bytes")
                else:
                    print(f"   ⚠️  PDF seems small: {len(response.content)} bytes")
            else:
                print(f"   ❌ Wrong content type: {content_type}")
                
        return success

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Wasla Phase 3 Backend API Tests")
        print("=" * 50)
        
        # Login first
        if not self.login():
            print("❌ Cannot proceed without authentication")
            return False
            
        # Test all endpoints
        tests = [
            self.test_csv_template_download,
            self.test_import_index_page,
            self.test_themes_list_page,
            self.test_theme_selection,
            self.test_branding_edit_page,
            self.test_branding_form_submission,
            self.test_exports_index_page,
            self.test_orders_csv_export,
            self.test_pdf_invoice_generation
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with error: {e}")
                
        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return False

def main():
    """Main test runner"""
    tester = WaslaAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())