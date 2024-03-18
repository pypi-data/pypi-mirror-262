import time
import unittest
from unittest.mock import Mock
from model_meter import ModelMeter

class TestModelMeter(unittest.TestCase):
    def test_measure(self):
        # Create a mock instance of the model
        mock_model = Mock()

        # Set up side_effect to simulate model call time
        def mock_model_call(image, *args, **kwargs):
            time.sleep(0.1)  # Assume 0.1 seconds per model call
            return "mock_result"

        mock_model.side_effect = mock_model_call

        # Create an instance of ModelMeter
        meter = ModelMeter(mock_model)
        mock_image = "image"
        # Test the measure function
        throughput, avg_time_per_image = meter.measure(params=(mock_image), method_name="__call__", min_iterations=5, max_duration=1)
        
        # Verify the results
        self.assertTrue(throughput > 0)
        self.assertTrue(avg_time_per_image > 0)
        self.assertTrue(mock_model.call_count >= 5) 

if __name__ == '__main__':
    unittest.main()
