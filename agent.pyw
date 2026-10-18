import os
import time
import math
import random
import ctypes
from datetime import datetime, timedelta


# NATIVE WINDOWS INPUT SIMULATION (Zero External Dependencies)


PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

INPUT_KEYBOARD = 1
INPUT_MOUSE = 0
KEYEVENTF_KEYUP = 0x0002
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

VK_CTRL = 0x11
VK_ALT = 0x12
VK_WIN = 0x5B
VK_ENTER = 0x0D
VK_BACK = 0x08
VK_TAB = 0x09
VK_SPACE = 0x20

def send_key_down(vk):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(vk, ctypes.windll.user32.MapVirtualKeyW(vk, 0), 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_KEYBOARD), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def send_key_up(vk):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(vk, ctypes.windll.user32.MapVirtualKeyW(vk, 0), KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_KEYBOARD), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press_key(vk):
    send_key_down(vk)
    time.sleep(0.04)
    send_key_up(vk)

def press_hotkey(*vks):
    for vk in vks:
        send_key_down(vk)
        time.sleep(0.04)
    for vk in reversed(vks):
        send_key_up(vk)
        time.sleep(0.04)

def type_char(c):
    if c == '\n':
        press_key(VK_ENTER)
        return
    if c == ' ':
        press_key(VK_SPACE)
        return
    vk = ctypes.windll.user32.VkKeyScanW(ord(c))
    if vk == -1:
        return
    virtual_key = vk & 0xFF
    shift_needed = (vk & 0x100) != 0
    
    if shift_needed:
        send_key_down(0x10)
    press_key(virtual_key)
    if shift_needed:
        send_key_up(0x10)

def scroll_wheel(amount):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, int(amount * 120), MOUSEEVENTF_WHEEL, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(INPUT_MOUSE), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def click_mouse():
    extra = ctypes.c_ulong(0)
    ii_d = Input_I()
    ii_d.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
    xd = Input(ctypes.c_ulong(INPUT_MOUSE), ii_d)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(xd), ctypes.sizeof(xd))
    time.sleep(0.05)
    ii_u = Input_I()
    ii_u.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
    xu = Input(ctypes.c_ulong(INPUT_MOUSE), ii_u)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(xu), ctypes.sizeof(xu))


 
# CONFIGURATION & DATA (Whitelisted Websites Only)
 
ALLOWED_WEBSITES = [
    "https://www.coinmarketcap.com",
    "https://www.coursera.org",
    "https://www.coinbase.com",
    "https://coingecko.com",
    "https://www.samsung.com",
    "https://aws.amazon.com",
    "https://www.amazon.com",
    "https://www.apple.com",
    "https://apnews.com",
    "https://www.dell.com"
]

WORD_APP = "swriter"      # OpenOffice Writer
EXCEL_APP = "scalc"       # OpenOffice Calc

SEARCH_QUERIES = [
    "pricing details",
    "support documentation",
    "recent updates",
    "product catalog",
    "system status"
]

QWERTY_NEIGHBORS = {
    'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'ersfxc', 'e': 'wsdr',
    'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujnbg', 'i': 'ujko', 'j': 'uikmnh',
    'k': 'ijlm', 'l': 'okp', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'wedxza', 't': 'rfgy',
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu', 'z': 'asx'
}

REPORT_PARAGRAPHS = [
    "Q3 Infrastructure Review: All virtualized nodes are operating within normal memory thresholds.",
    "Telemetry analysis confirms that user session processes are cleanly initiated from the desktop shell.",
    "Network traffic remains restricted to approved internal and whitelisted external endpoints.",
    "Action items for next week include reviewing storage allocations and updating baseline snapshots."
]

SPREADSHEET_ROWS = [
    ["Metric", "Target", "Actual", "Status"],
    ["CPU Load", "25%", "14%", "Optimal"],
    ["Memory Usage", "4096MB", "2850MB", "Normal"],
    ["Latency", "45ms", "38ms", "Pass"],
    ["Uptime", "99.9%", "100.0%", "Verified"]
]

# TIMING & HUMAN ENTROPY

def gaussian_delay(mean=1.5, std_dev=0.4, min_val=0.4, max_val=4.0):
    delay = random.gauss(mean, std_dev)
    delay = max(min_val, min(delay, max_val))
    time.sleep(delay)

def uniform_delay(min_sec=0.8, max_sec=2.5):
    time.sleep(random.uniform(min_sec, max_sec))

def keystroke_delay():
    delay = max(0.04, min(random.gauss(0.12, 0.05), 0.38))
    time.sleep(delay)

def type_with_typos(text, allow_typos=True):
    for char in text:
        if allow_typos and char.lower() in QWERTY_NEIGHBORS and random.random() < 0.04:
            wrong_char = random.choice(QWERTY_NEIGHBORS[char.lower()])
            type_char(wrong_char)
            keystroke_delay()
            
            if random.random() < 0.35:
                type_char(char)
                keystroke_delay()
                time.sleep(random.uniform(0.25, 0.6))
                press_key(VK_BACK)
                keystroke_delay()
            else:
                time.sleep(random.uniform(0.2, 0.5))
            
            press_key(VK_BACK)
            time.sleep(random.uniform(0.1, 0.3))

        type_char(char)
        keystroke_delay()

        if char in ['.', ',', ':']:
            gaussian_delay(mean=0.6, std_dev=0.2, min_val=0.3, max_val=1.2)
        elif char == ' ' and random.random() < 0.12:
            gaussian_delay(mean=0.4, std_dev=0.15, min_val=0.2, max_val=0.9)



# PROCESS AUTHENTICITY & WINDOW MANAGEMENT LAUNCHERS


def maximize_window():
    """Maximizes whatever application window is currently active (Win + Up)."""
    press_hotkey(VK_WIN, 0x26)
    uniform_delay(0.5, 1.0)

def launch_chrome():
    os.startfile("chrome.exe")
    gaussian_delay(mean=3.5, std_dev=0.8, min_val=2.5, max_val=5.0)
    maximize_window()

def launch_via_explorer(command_str):
    press_hotkey(VK_WIN, ord('R'))
    gaussian_delay(mean=1.0, std_dev=0.25, min_val=0.6, max_val=1.8)
    
    press_key(VK_BACK)
    time.sleep(random.uniform(0.1, 0.3))
    
    type_with_typos(command_str, allow_typos=False)
    uniform_delay(0.3, 0.7)
    press_key(VK_ENTER)



# WORKFLOWS


def simulate_word_document():
    launch_via_explorer(WORD_APP)
    gaussian_delay(mean=4.5, std_dev=1.0, min_val=3.0, max_val=7.0)
    maximize_window() # Fullscreen OpenOffice Writer

    selected_paragraphs = random.sample(REPORT_PARAGRAPHS, random.randint(2, 3))
    for para in selected_paragraphs:
        type_with_typos(para, allow_typos=True)
        press_key(VK_ENTER)
        press_key(VK_ENTER)
        gaussian_delay(mean=1.8, std_dev=0.5, min_val=1.0, max_val=3.5)

    press_hotkey(VK_CTRL, ord('S'))
    gaussian_delay(mean=2.0, std_dev=0.4, min_val=1.2, max_val=3.0)

    doc_name = f"ops_summary_{random.randint(100, 999)}"
    type_with_typos(doc_name, allow_typos=False)
    uniform_delay(0.6, 1.4)
    press_key(VK_ENTER)

    gaussian_delay(mean=2.5, std_dev=0.5, min_val=1.8, max_val=4.0)
    press_hotkey(VK_ALT, 0x73) # Alt + F4
    uniform_delay(1.0, 2.5)

def simulate_spreadsheet():
    launch_via_explorer(EXCEL_APP)
    gaussian_delay(mean=4.5, std_dev=1.0, min_val=3.0, max_val=7.0)
    maximize_window() # Fullscreen OpenOffice Calc

    for row in SPREADSHEET_ROWS:
        for col_idx, cell_value in enumerate(row):
            type_with_typos(cell_value, allow_typos=True)
            uniform_delay(0.2, 0.6)
            if col_idx < len(row) - 1:
                press_key(VK_TAB)
                uniform_delay(0.2, 0.5)
        
        press_key(VK_ENTER)
        for _ in range(len(row) - 1):
            press_key(0x25)
            time.sleep(random.uniform(0.05, 0.12))
        gaussian_delay(mean=1.0, std_dev=0.3, min_val=0.5, max_val=2.0)

    press_hotkey(VK_CTRL, ord('S'))
    gaussian_delay(mean=2.0, std_dev=0.4, min_val=1.2, max_val=3.0)

    sheet_name = f"metrics_log_{random.randint(100, 999)}"
    type_with_typos(sheet_name, allow_typos=False)
    uniform_delay(0.6, 1.4)
    press_key(VK_ENTER)

    gaussian_delay(mean=2.5, std_dev=0.5, min_val=1.8, max_val=4.0)
    press_hotkey(VK_ALT, 0x73)
    uniform_delay(1.0, 2.5)

def simulate_web_surfing():
    launch_chrome() # Launches and fullscreens Chrome automatically

    session_sites = random.sample(ALLOWED_WEBSITES, random.randint(1, 2))
    for idx, url in enumerate(session_sites):
        if idx > 0 and random.random() < 0.5:
            press_hotkey(VK_CTRL, ord('T'))
            uniform_delay(0.6, 1.2)
        else:
            press_hotkey(VK_CTRL, ord('L'))
            uniform_delay(0.4, 0.9)

        type_with_typos(url, allow_typos=False)
        uniform_delay(0.3, 0.7)
        press_key(VK_ENTER)

        gaussian_delay(mean=4.5, std_dev=1.2, min_val=3.0, max_val=7.5)

        for _ in range(random.randint(2, 4)):
            scroll_wheel(random.choice([-5, -3, 3]))
            gaussian_delay(mean=2.2, std_dev=0.7, min_val=1.0, max_val=4.5)

        click_mouse()
        uniform_delay(0.4, 0.9)
        press_hotkey(VK_CTRL, ord('F'))
        uniform_delay(0.5, 1.0)
        
        query = random.choice(SEARCH_QUERIES)
        type_with_typos(query, allow_typos=True)
        uniform_delay(0.5, 1.2)
        press_key(VK_ENTER)
        
        gaussian_delay(mean=2.0, std_dev=0.5, min_val=1.0, max_val=3.0)

    press_hotkey(VK_ALT, 0x73)
    uniform_delay(1.0, 2.0)


# ORCHESTRATOR - 17min run time


def main():
    end_time = datetime.now() + timedelta(minutes=17)
    time.sleep(random.uniform(3.0, 5.0))

    cycle_count = 0
    while datetime.now() < end_time:
        cycle_count += 1
        if cycle_count % 2 == 1:
            simulate_web_surfing()
        else:
            if random.random() < 0.65:
                simulate_word_document()
            else:
                simulate_spreadsheet()
        gaussian_delay(mean=6.0, std_dev=2.0, min_val=3.5, max_val=11.0)

if __name__ == "__main__":
    main()
