import time

def run_mouse_test():
    print("Starting Standalone Mouse Control Diagnostics...\n")
    
    # Try importing pynput
    try:
        from pynput.mouse import Controller as PynputController
        pynput_mouse = PynputController()
        has_pynput = True
        print("[OK] pynput imported successfully.")
    except Exception as e:
        print(f"[FAIL] Failed to import pynput: {e}")
        has_pynput = False

    # Try importing pyautogui
    try:
        import pyautogui
        pyautogui.FAILSAFE = False
        has_pyautogui = True
        print("[OK] pyautogui imported successfully.")
        
        # Get screen size
        width, height = pyautogui.size()
        print(f"Screen Resolution Detected: {width}x{height}")
    except Exception as e:
        print(f"[FAIL] Failed to import pyautogui: {e}")
        has_pyautogui = False
        width, height = 1920, 1080
        print(f"Defaulting Screen Resolution to: {width}x{height}")
        
    if not has_pynput and not has_pyautogui:
        print("\nCRITICAL FAILURE: Neither pynput nor pyautogui is available.")
        print("Cannot control the mouse. Please install them using 'pip install pynput pyautogui'.")
        return

    positions = [
        ("Center", int(width/2), int(height/2)),
        ("Top Left", 100, 100),
        ("Top Right", int(width - 100), 100),
        ("Bottom Right", int(width - 100), int(height - 100)),
        ("Bottom Left", 100, int(height - 100)),
        ("Center", int(width/2), int(height/2))
    ]

    print("\nStarting physical cursor movement test...")
    print("WARNING: Do NOT move your physical mouse during this test.")
    time.sleep(2)

    backends_to_test = []
    if has_pynput: backends_to_test.append("pynput")
    if has_pyautogui: backends_to_test.append("pyautogui")

    for backend in backends_to_test:
        print(f"\n--- Testing Backend: {backend.upper()} ---")
        
        test_failed = False
        for name, x, y in positions:
            print(f"Moving to {name} ({x}, {y})...", end="")
            
            try:
                if backend == "pynput":
                    pynput_mouse.position = (x, y)
                elif backend == "pyautogui":
                    pyautogui.moveTo(x, y, _pause=False)
                    
                time.sleep(0.5)
                print(" OK")
            except Exception as e:
                print(f" FAILED!\nError: {e}")
                test_failed = True
                break
                
        if test_failed:
            print(f"\n[!] Backend {backend} failed to move the cursor.")
            print("This usually means Windows security, another application, or a permission issue is blocking mouse control.")
        else:
            print(f"\n[SUCCESS] Backend {backend} completed all movements successfully!")
            
    print("\nDiagnostics complete.")

if __name__ == "__main__":
    run_mouse_test()
