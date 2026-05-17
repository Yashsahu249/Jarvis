import pytest

from jarvis.voice.lang_detect import detect_language
from jarvis.voice.wake import WakeWordDetector
from jarvis.utils.helpers import detect_language as util_detect_language


def test_language_detection_english():
    assert detect_language("Hello, how are you?") == "english"
    assert util_detect_language("This is a test") == "english"


def test_language_detection_hindi():
    assert detect_language("नमस्ते, आप कैसे हैं?") == "hindi"
    assert util_detect_language("मैं ठीक हूँ") == "hindi"


def test_language_detection_hinglish():
    assert detect_language("Hello, आप कैसे हैं?") == "hinglish"
    assert util_detect_language("Yeh बहुत achha hai bro") == "hinglish"


def test_language_detection_empty():
    assert detect_language("") == "unknown"
    assert detect_language("   ") == "unknown"


def test_wake_word_detection():
    detector = WakeWordDetector()
    assert detector.contains_wake_word("jarvis, hello")
    assert detector.contains_wake_word("Hey Jarvis!")
    assert not detector.contains_wake_word("hello there")


def test_strip_wake_word():
    detector = WakeWordDetector()
    assert detector.strip_wake_word("jarvis hello") == " hello"
    assert detector.strip_wake_word("Jarvis, what's up") == ", what's up"
