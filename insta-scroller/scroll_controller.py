"""
scroll_controller.py
--------------------
هر اشاره = یه اسکرول به پایین (ریلز بعدی).
دیگه بین UP و DOWN تفاوتی نیست.
"""

try:
    import pyautogui
    pyautogui.PAUSE = 0
    _PYAUTOGUI_OK = True
except Exception as exc:
    _PYAUTOGUI_OK = False
    _PYAUTOGUI_ERROR = exc

from gesture_detector import DOWN, IDLE


class ScrollController:
    def __init__(self, config):
        self.amount = config.SCROLL_AMOUNT

        if not _PYAUTOGUI_OK:
            raise RuntimeError(
                "pyautogui import نشد. با این دستور نصبش کن:\n"
                "    pip install pyautogui\n"
                f"خطای اصلی: {_PYAUTOGUI_ERROR}"
            )

    def handle(self, direction):
        """
        direction: DOWN یا IDLE
        هر اشاره -> یه اسکرول به پایین
        """
        if direction == DOWN:
            pyautogui.scroll(-self.amount)
            return DOWN
        return None