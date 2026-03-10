import pyautogui

# Set a small delay after each pyautogui call for safety
pyautogui.PAUSE = 0.5

def click(x: int, y: int):
    """
    Moves the mouse to the specified coordinates and clicks.
    """
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()
    return f"Clicked at ({x}, {y})"

def type_text(text: str):
    """
    Types the specified text.
    """
    pyautogui.write(text, interval=0.05)
    return f"Typed: '{text}'"

def press_key(key: str):
    """
    Presses a specific key (e.g., 'enter', 'tab', 'shift').
    """
    pyautogui.press(key)
    return f"Pressed key: {key}"

def scroll(amount: int):
    """
    Scrolls the screen by the given amount.
    """
    pyautogui.scroll(amount)
    return f"Scrolled by {amount}"
