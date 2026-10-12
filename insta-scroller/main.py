"""
main.py
-------
ورودی برنامه. ماژول‌ها رو به هم وصل می‌کنه.
کلید Q برای خروج.
"""

import time

import cv2

import config
from camera import Camera
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from scroll_controller import ScrollController


def draw_debug(frame, hand, direction, scroll, fps):
    lines = [f"Hand: {'Detected' if hand else 'None'}"]
    if hand:
        lines.append(f"Pos: ({hand['pixel_x']}, {hand['pixel_y']})")
    lines.append(f"Gesture: {direction}")
    lines.append(f"Scroll: {scroll if scroll else '-'}")
    lines.append(f"FPS: {int(fps)}")

    y = 30
    for line in lines:
        cv2.putText(frame, line, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2, cv2.LINE_AA)
        y += 30


def main():
    camera = Camera(
        index=config.CAMERA_INDEX,
        width=config.CAMERA_WIDTH,
        height=config.CAMERA_HEIGHT,
        mirror=config.MIRROR_CAMERA,
    )
    try:
        camera.open()
    except RuntimeError as err:
        print(f"[camera error] {err}")
        return

    tracker = HandTracker(config)
    detector = GestureDetector(config)

    try:
        scroller = ScrollController(config)
    except RuntimeError as err:
        print(err)
        camera.release()
        tracker.close()
        return

    prev_time = time.time()
    fps = 0.0

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("[camera] failed to read a frame, exiting")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand = tracker.find_hand(rgb)

            now = time.time()

            if hand is not None:
                tracker.draw(frame, hand["landmarks"])
                cv2.circle(frame,
                           (hand["pixel_x"], hand["pixel_y"]),
                           8, (0, 255, 0), -1)
                direction = detector.update(hand["y"], now)
            else:
                direction = detector.update(None, now)

            applied = scroller.handle(direction)

            dt = now - prev_time
            prev_time = now
            if dt > 0:
                fps = 0.9 * fps + 0.1 * (1.0 / dt)

            if config.DEBUG:
                draw_debug(frame, hand, direction, applied, fps)

            cv2.imshow("Hand Scroll - press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        camera.release()
        tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()