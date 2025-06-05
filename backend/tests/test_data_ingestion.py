import unittest
import json
from app import create_app # Assuming run.py and tests are in a place where 'app' can be imported

class DataIngestionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        # If create_app takes arguments (e.g. for config), adjust here.
        # For now, assuming a simple create_app() as defined in previous steps.

    def test_receive_eye_tracking_data(self):
        payload = {"user_id": "test_user_1", "timestamp": "2024-07-30T10:00:00Z", "gaze_point": {"x": 120, "y": 340}}
        response = self.client.post('/api/ingestion/data/eye_tracking',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response['message'], "Eye tracking data received and processed")
        self.assertIn('data', json_response)
        self.assertEqual(json_response['data']['user_id'], "test_user_1")

    def test_receive_voice_analysis_data(self):
        payload = {"user_id": "test_user_2", "timestamp": "2024-07-30T10:05:00Z", "transcript": "Hello world", "confidence": 0.95}
        response = self.client.post('/api/ingestion/data/voice_analysis',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response['message'], "Voice analysis data received and processed")
        self.assertIn('data', json_response)
        self.assertEqual(json_response['data']['user_id'], "test_user_2")

if __name__ == '__main__':
    unittest.main()
