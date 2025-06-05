import React, { useState } from 'react';

// Mock data for initial state
const initialMockEyeTrackingData = {
  user_id: "user123",
  session_id: "sessionABC",
  // other fields from your previous mock if needed by other components,
  // but for this form, only user_id and session_id are directly used from here.
};

const initialDefaultEyeDataJSON = JSON.stringify({
  duration_seconds: 30,
  gaze_events: [
    { type: "fixation", x: 300, y: 400, duration: 250, timestamp: "2024-07-31T10:00:01Z", pupil_size: 3.5 },
    { type: "saccade", start_x: 300, start_y: 400, end_x: 600, end_y: 400, duration: 30, timestamp: "2024-07-31T10:00:01.250Z" }
  ],
  raw_pupil_sizes: [3.5, 3.6, 3.7, 3.5], // Example: ensure this matches what backend might expect
  blinks_count: 1
}, null, 2);

function EyeTrackingForm() {
  const [userId, setUserId] = useState(initialMockEyeTrackingData.user_id);
  const [sessionId, setSessionId] = useState(initialMockEyeTrackingData.session_id);
  const [eyeDataJson, setEyeDataJson] = useState(initialDefaultEyeDataJSON);
  const [responseMessage, setResponseMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setResponseMessage(''); // Clear previous messages

    let parsedEyeData;
    try {
      parsedEyeData = JSON.parse(eyeDataJson);
    } catch (error) {
      console.error("Error parsing Eye Data JSON:", error);
      setResponseMessage(`Error parsing JSON: ${error.message}`);
      return;
    }

    const payload = {
      user_id: userId,
      session_id: sessionId,
      ...parsedEyeData
    };

    try {
      // Using relative path, assuming proxy setup or same-origin deployment
      const response = await fetch('/api/ingestion/data/eye_tracking', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json(); // Or response.text() if not always JSON

      if (!response.ok) {
        console.error("Backend error:", result);
        setResponseMessage(`Error from backend: ${result.message || response.statusText}`);
      } else {
        console.log("Backend success:", result);
        // Example: Highlighting extracted features
        const features = result.data.extracted_eye_features;
        const featureString = Object.entries(features).map(([key, value]) => `${key}: ${typeof value === 'number' ? value.toFixed(2) : value}`).join(', ');
        setResponseMessage(`Success: ${result.message}. Extracted Features: ${featureString}`);
      }
    } catch (error) {
      console.error("Network or other error:", error);
      setResponseMessage(`Network error: ${error.message}`);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-700">Eye-Tracking Data Submission</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="user_id" className="block text-sm font-medium text-gray-700 mb-1">User ID</label>
          <input
            type="text"
            id="user_id"
            name="user_id"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="session_id" className="block text-sm font-medium text-gray-700 mb-1">Session ID</label>
          <input
            type="text"
            id="session_id"
            name="session_id"
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <div className="mb-6">
          <label htmlFor="eye_data_json" className="block text-sm font-medium text-gray-700 mb-1">Eye-Tracking Details (JSON)</label>
          <textarea
            id="eye_data_json"
            name="eye_data_json"
            rows="10"
            value={eyeDataJson}
            onChange={(e) => setEyeDataJson(e.target.value)}
            className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm font-mono"
            placeholder="Enter eye-tracking event data as JSON..."
          />
          <p className="mt-1 text-xs text-gray-500">
            Include fields like duration_seconds, gaze_events, raw_pupil_sizes, blinks_count.
          </p>
        </div>

        <button
          type="submit"
          className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Submit Data
        </button>
      </form>
      {responseMessage && (
        <div className={`mt-6 p-4 rounded-md ${responseMessage.startsWith('Error') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          <h3 className="text-lg font-semibold mb-2">Submission Status:</h3>
          <pre className="whitespace-pre-wrap break-all text-sm">{responseMessage}</pre>
        </div>
      )}
    </div>
  );
}

export default EyeTrackingForm;
