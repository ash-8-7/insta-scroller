"""
config.py
---------
تنظیمات پروژه. فقط این فایل رو تغییر بده.
"""

# ---------- Camera ----------
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
MIRROR_CAMERA = True

# ---------- MediaPipe ----------
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# ---------- Gesture detector (حالت اشاره) ----------
# چقدر دست باید از حالت خنثی فاصله بگیره تا یه اشاره حساب بشه.
# عدد بزرگ‌تر = باید دستت رو واضح‌تر ببری
SWIPE_THRESHOLD = 0.12

# نرم‌کننده: کمتر = نرم‌تر ولی کندتر
SMOOTHING_FACTOR = 0.30

# وقتی دستت به این فاصله از نقطهٔ خنثی برگرده،
# می‌تونه اشارهٔ بعدی رو انجام بده (ریست میشه)
RESET_THRESHOLD = 0.05

# حداقل فاصله بین دو اشاره (ثانیه)
# جلوگیری می‌کنه که یه حرکت، چند اسکرول بفرسته
SWIPE_COOLDOWN = 1.8

# ---------- Scroll controller ----------
# مقدار اسکرول هر اشاره (به «کلیک» pyautogui)
# این رو با آزمون و خطا تنظیم کن:
#   اینستاگرام معمولاً با 300 تا 600 یه پست میره
SCROLL_AMOUNT = 350

# ---------- Debug ----------
DEBUG = True