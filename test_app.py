import unittest
import json
import os
import sys
from app import app, load_data

class VendorQualificationAPITests(unittest.TestCase):
    """Test suite for the Vendor Qualification API."""
    
    def setUp(self):
        """Set up test client and ensure data is loaded."""
        self.app = app.test_client()
        self.app.testing = True
       
        load_data()
    
    def test_health_endpoint(self):
        """Test that the health endpoint returns a successful response."""
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('message', data)
    
    def test_vendor_qualification_no_filters(self):
        """Test vendor qualification with no filters returns top vendors by rating."""
        response = self.app.post('/vendor_qualification',
                            data=json.dumps({}),
                            content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        self.assertIn('top_vendors', data['data'])
        self.assertIn('count', data['data'])

        # this code will  return up to 10 vendors sorted by rating 
        self.assertLessEqual(data['data']['count'], 10)
    
    def test_vendor_qualification_by_category(self):
        """Test filtering vendors by software category."""
        response = self.app.post('/vendor_qualification',
                            data=json.dumps({"software_category": "CRM"}),
                            content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

        # Verifying  all returned vendors are in the CRM category
        for vendor in data['data']['top_vendors']:
            self.assertIn("CRM", vendor['main_category'])
    
    def test_vendor_qualification_by_capabilities(self):
        """Test filtering vendors by capabilities."""
        response = self.app.post('/vendor_qualification',
                            data=json.dumps({"capabilities": ["custom objects"]}),
                            content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

        # Verifying  the capability appears in all returned vendors' features
        for vendor in data['data']['top_vendors']:
            self.assertIn("custom objects", vendor['parsed_features'].lower())
    
    def test_vendor_qualification_combined_filters(self):
        """Test filtering vendors by both category and capabilities."""
        response = self.app.post('/vendor_qualification',
                            data=json.dumps({
                                "software_category": "CRM",
                                "capabilities": ["custom objects"]
                            }),
                            content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        # Verifying the  results meet both criteria
        for vendor in data['data']['top_vendors']:
            self.assertIn("CRM", vendor['main_category'])
            self.assertIn("custom objects", vendor['parsed_features'].lower())
    
    def test_vendor_qualification_nonexistent_category(self):
        """Test with a category that doesn't exist in the dataset."""
        response = self.app.post('/vendor_qualification',
                            data=json.dumps({"software_category": "NonexistentCategory"}),
                            content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        self.assertEqual(data['data']['count'], 0)
        self.assertEqual(data['data']['top_vendors'], [])
    
    def test_invalid_json_format(self):
        """Test handling of invalid JSON in request."""
        response = self.app.post('/vendor_qualification',
                            data="Invalid JSON",
                            content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
    
    def test_rating_order(self):
        """Test that vendors are returned in descending order by rating."""
        response = self.app.post('/vendor_qualification',
                            data=json.dumps({}),
                            content_type='application/json')
        data = json.loads(response.data)
        
        vendors = data['data']['top_vendors']
        if len(vendors) > 1:  # This will Only test if we have multiple vendors
            for i in range(len(vendors) - 1):
                self.assertGreaterEqual(
                    vendors[i]['rating'], 
                    vendors[i+1]['rating'],
                    "Vendors should be sorted by rating in descending order"
                )

if __name__ == '__main__':
    unittest.main()