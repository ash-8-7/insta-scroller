"""
hand_tracker.py
---------------
Wraps MediaPipe Hands and exposes a small, MediaPipe-agnostic interface:

    find_hand(rgb_frame) -> dict | None
        {
          "x": float,          # normalized palm-center X in [0,1]
          "y": float,          # normalized palm-center Y in [0,1]
          "pixel_x": int,
          "pixel_y": int,
          "landmarks": <raw landmarks object>
        }

If you ever swap MediaPipe for another hand-tracking library, keep this
same dict shape and nothing else in the project needs to change.
"""

import mediapipe as mp


class HandTracker:
    # Landmarks averaged to find the "palm center".
    # 0  = wrist
    # 5  = index  finger MCP
    # 9  = middle finger MCP
    # 13 = ring   finger MCP
    # 17 = pinky  finger MCP
    PALM_LANDMARK_IDS = (0, 5, 9, 13, 17)

    def __init__(self, config):
        self._mp_hands = mp.solutions.hands
        self._mp_draw = mp.solutions.drawing_utils
        self._hands = self._mp_hands.Hands(
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
        )

    def find_hand(self, rgb_frame):
        """Return a dict describing the hand, or None if no hand found."""
        results = self._hands.process(rgb_frame)
        if not results.multi_hand_landmarks:
            return None

        hand = results.multi_hand_landmarks[0]
        h, w = rgb_frame.shape[:2]

        xs, ys = [], []
        for idx in self.PALM_LANDMARK_IDS:
            lm = hand.landmark[idx]
            xs.append(lm.x)
            ys.append(lm.y)

        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)

        return {
            "x": cx,
            "y": cy,
            "pixel_x": int(cx * w),
            "pixel_y": int(cy * h),
            "landmarks": hand,
        }

    def draw(self, bgr_frame, landmarks):
        """Draw the hand skeleton on a BGR frame (for the debug window)."""
        self._mp_draw.draw_landmarks(
            bgr_frame, landmarks, self._mp_hands.HAND_CONNECTIONS
        )

    def close(self):
        self._hands.close()