from flask import Flask, request, jsonify
from flask_cors import CORS
import mediapipe as mp
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

# Initialize MediaPipe Pose model.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)


def analyze_posture(image):
    print("===================================================")
    # Get height and width of the frame.
    h, w = image.shape[:2]
    # Convert the image to RGB.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Process image to find poses.
    results = pose.process(image_rgb)
    lm = results.pose_landmarks
    lmPose = mp_pose.PoseLandmark
    if lm:
        # Left shoulder.
        l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

        # Right shoulder.
        r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

        # Left ear.
        l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
        l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)

        # Left hip.
        l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
        l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)


        # Placeholder for posture analysis logic.
        # Implement actual posture checking logic here.

        print(f'Left Shoulder X position: {l_shldr_x}')
        print(f'Left Hip X position: {l_hip_x}')
        print(f'Horizontal Distance : {abs(l_shldr_x - l_hip_x)}')

        if abs(l_shldr_x - l_hip_x) > 15:
            print("Person Detected, bad posture")
            return True, False
        print("Person Detected, good posture")
        return True, True
    print("No person detected")
    return False, False


@app.route('/analyze', methods=['POST'])
def analyze_image():
    # Check if an image is part of the request.
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Read the image file.
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Analyze the posture.
    person_detected, posture_description = analyze_posture(image)

    return jsonify({
        'person_detected': person_detected,
        'posture_description': posture_description
    })


if __name__ == '__main__':
    app.run(debug=True)
