"""
gesture_detector.py
-------------------
حالت «اشاره» با یه تغییر مهم:
    - چه دستت بالا بره چه پایین، همیشه یه DOWN برمی‌گردونه
    - یعنی هر اشاره = رفتن به ریلز بعدی

منطق:
    1. دستت رو از حالت خنثی دور کن (بالا یا پایین)
    2. برنامه یه DOWN برمی‌گردونه
    3. تا SWIPE_COOLDOWN ثانیه و برگشتن دست به حالت خنثی، قفل میشه
"""

UP = "UP"        # (دیگه استفاده نمیشه، ولی برای سازگاری نگه داشتم)
DOWN = "DOWN"
IDLE = "IDLE"


class GestureDetector:
    def __init__(self, config):
        self.smoothing = config.SMOOTHING_FACTOR
        self.swipe_threshold = config.SWIPE_THRESHOLD
        self.reset_threshold = config.RESET_THRESHOLD
        self.cooldown = config.SWIPE_COOLDOWN

        self.smoothed_y = None
        self.neutral_y = None
        self.last_swipe_time = 0.0
        self.armed = True

    def _update_neutral(self, y):
        if self.neutral_y is None:
            self.neutral_y = y
        else:
            self.neutral_y = 0.05 * y + 0.95 * self.neutral_y

    def update(self, hand_y, now):
        """
        hand_y: مختصات Y نرمال‌شده (0..1) یا None
        now: زمان فعلی (ثانیه)
        خروجی: DOWN (اشاره) یا IDLE
        """
        if hand_y is None:
            self.smoothed_y = None
            self.armed = True
            return IDLE

        if self.smoothed_y is None:
            self.smoothed_y = hand_y
            self._update_neutral(hand_y)
            return IDLE

        self.smoothed_y = (
            self.smoothing * hand_y
            + (1.0 - self.smoothing) * self.smoothed_y
        )

        self._update_neutral(hand_y)

        # در حال خنک‌شدن؟
        if not self.armed:
            if now - self.last_swipe_time < self.cooldown:
                return IDLE
            delta = self.smoothed_y - self.neutral_y
            if abs(delta) < self.reset_threshold:
                self.armed = True
            return IDLE

        # محاسبهٔ فاصله از نقطهٔ خنثی
        delta = self.smoothed_y - self.neutral_y

        # هر دو جهت -> DOWN (ریلز بعدی)
        if abs(delta) > self.swipe_threshold:
            self.armed = False
            self.last_swipe_time = now
            return DOWN

        return IDLE