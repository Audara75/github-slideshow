import unittest
import numpy as np
from app.data_ingestion.processing import process_eye_tracking_data, process_voice_analysis_data

class TestProcessingFunctions(unittest.TestCase):

    def test_eye_tracking_with_data(self):
        sample_data = {
            "gaze_events": [
                {"type": "fixation", "duration": 200},
                {"type": "fixation", "duration": 300},
                {"type": "saccade"},
            ],
            "raw_pupil_sizes": [3.0, 3.5, 4.0],
            "blinks_count": 2,
            "duration_seconds": 10
        }
        result = process_eye_tracking_data(sample_data.copy()) # Use .copy() to avoid modifying original dict in other tests
        self.assertIn('extracted_eye_features', result)
        features = result['extracted_eye_features']
        self.assertAlmostEqual(features['fixation_duration_avg'], 250.0)
        self.assertAlmostEqual(features['saccade_frequency'], 0.1) # 1 saccade / 10s
        self.assertAlmostEqual(features['pupil_dilation_avg'], 3.5)
        self.assertAlmostEqual(features['blink_rate'], 12.0) # (2 blinks / 10s) * 60

    def test_eye_tracking_empty_data(self):
        result = process_eye_tracking_data({})
        self.assertIn('extracted_eye_features', result)
        features = result['extracted_eye_features']
        self.assertEqual(features['fixation_duration_avg'], 250.0) # Default
        self.assertEqual(features['saccade_frequency'], 0.0)     # Calculated: 0 saccades / 30s default duration
        self.assertEqual(features['pupil_dilation_avg'], 3.5)    # Default
        self.assertEqual(features['blink_rate'], 0.0)         # Calculated: 0 blinks / 30s default duration

    def test_eye_tracking_default_blink_rate_scenario(self):
        # Test case where duration is 0, triggering explicit defaults
        result = process_eye_tracking_data({'duration_seconds': 0})
        self.assertIn('extracted_eye_features', result)
        features = result['extracted_eye_features']
        self.assertEqual(features['saccade_frequency'], 3.0) # Default due to duration_seconds = 0
        self.assertEqual(features['blink_rate'], 15.0) # Default due to duration_seconds = 0


    def test_voice_analysis_with_data(self):
        sample_data = {
            "word_count": 100,
            "duration_seconds": 30,
            "pitch_values": [100, 110, 120, 105, 115],
            "pause_timestamps": [{}, {}, {}] # 3 pauses
        }
        result = process_voice_analysis_data(sample_data.copy())
        self.assertIn('extracted_voice_features', result)
        features = result['extracted_voice_features']
        self.assertAlmostEqual(features['speech_rate'], 200.0) # (100 / 30) * 60
        self.assertTrue(np.isclose(features['pitch_variation'], np.std([100,110,120,105,115])))
        self.assertAlmostEqual(features['pause_frequency'], 6.0) # (3 / 30) * 60
        self.assertEqual(features['confidence_score_mock'], 0.85) # Default

    def test_voice_analysis_empty_data(self):
        result = process_voice_analysis_data({})
        self.assertIn('extracted_voice_features', result)
        features = result['extracted_voice_features']
        self.assertEqual(features['speech_rate'], 150.0)    # Default
        self.assertEqual(features['pitch_variation'], 15.0) # Default
        self.assertEqual(features['pause_frequency'], 5.0)  # Default
        self.assertEqual(features['confidence_score_mock'], 0.85) # Default

    def test_voice_analysis_pitch_non_numeric(self):
        # Test with non-numeric and mixed pitch values
        sample_data_mixed = {"pitch_values": [100, "abc", 120, None, 130.5]}
        result_mixed = process_voice_analysis_data(sample_data_mixed.copy())
        features_mixed = result_mixed['extracted_voice_features']
        # Expecting std of [100, 120, 130.5] because non-numeric are filtered by the implementation
        self.assertTrue(np.isclose(features_mixed['pitch_variation'], np.std([100, 120, 130.5])))

        sample_data_all_non_numeric = {"pitch_values": ["abc", "def", None]}
        result_all_non_numeric = process_voice_analysis_data(sample_data_all_non_numeric.copy())
        features_all_non_numeric = result_all_non_numeric['extracted_voice_features']
        # Expecting default because all values are filtered out
        self.assertEqual(features_all_non_numeric['pitch_variation'], 15.0)


if __name__ == '__main__':
    unittest.main()
