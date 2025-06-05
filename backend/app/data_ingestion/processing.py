import numpy as np

def process_eye_tracking_data(data):
    print(f"Processing eye tracking data: {data}")
    extracted_features = {}

    # Simulate Fixation Duration Average
    fixations = [event['duration'] for event in data.get('gaze_events', []) if event.get('type') == 'fixation' and 'duration' in event]
    if fixations:
        extracted_features['fixation_duration_avg'] = np.mean(fixations)
    else:
        extracted_features['fixation_duration_avg'] = 250.0 # Default ms

    # Simulate Saccade Frequency
    saccades = [event for event in data.get('gaze_events', []) if event.get('type') == 'saccade']
    total_duration_seconds = data.get('duration_seconds', 30) # Default duration if not provided
    if total_duration_seconds > 0:
        extracted_features['saccade_frequency'] = len(saccades) / total_duration_seconds
    else:
        extracted_features['saccade_frequency'] = 3.0 # Default Hz

    # Simulate Pupil Dilation Average
    pupil_sizes = data.get('raw_pupil_sizes', [])
    if pupil_sizes:
        extracted_features['pupil_dilation_avg'] = np.mean(pupil_sizes)
    else:
        extracted_features['pupil_dilation_avg'] = 3.5 # Default mm

    # Simulate Blink Rate
    blinks_count = data.get('blinks_count', 0)
    # Use a local variable for duration to avoid potential division by zero if total_duration_seconds is 0
    # For blink rate, if duration is 0, it's problematic, so default.
    if total_duration_seconds > 0:
        extracted_features['blink_rate'] = (blinks_count / total_duration_seconds) * 60 # Blinks per minute
    else:
        extracted_features['blink_rate'] = 15.0 # Default blinks/min

    data['extracted_eye_features'] = extracted_features
    return data

def process_voice_analysis_data(data):
    print(f"Processing voice analysis data: {data}")
    extracted_features = {}

    # Simulate Speech Rate (words per minute)
    word_count = data.get('word_count')
    duration_seconds = data.get('duration_seconds')
    if word_count is not None and duration_seconds is not None and duration_seconds > 0:
        extracted_features['speech_rate'] = (word_count / duration_seconds) * 60
    else:
        extracted_features['speech_rate'] = 150.0  # Default wpm

    # Simulate Pitch Variation (standard deviation of pitch values)
    pitch_values = data.get('pitch_values', [])
    if pitch_values:
        # Ensure pitch_values are numeric for np.std
        numeric_pitch_values = [pv for pv in pitch_values if isinstance(pv, (int, float))]
        if numeric_pitch_values:
            extracted_features['pitch_variation'] = np.std(numeric_pitch_values)
        else:
            extracted_features['pitch_variation'] = 15.0 # Default if list empty or non-numeric
    else:
        extracted_features['pitch_variation'] = 15.0  # Default Hz

    # Simulate Pause Frequency (pauses per minute)
    pauses = data.get('pause_timestamps', []) # Assuming pause_timestamps is a list of occurrences
    if duration_seconds is not None and duration_seconds > 0:
        extracted_features['pause_frequency'] = (len(pauses) / duration_seconds) * 60
    else:
        # If duration_seconds is not available or zero, default pause_frequency
        extracted_features['pause_frequency'] = 5.0  # Default pauses/min

    # Simulate Confidence Score
    extracted_features['confidence_score_mock'] = data.get('confidence_score_mock', 0.85) # Allow override or default

    data['extracted_voice_features'] = extracted_features
    return data
