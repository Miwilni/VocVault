import sys
import os

if os.name == "nt":  # Windows
    import msvcrt
else:  # Linux/macOS
    import tty
    import termios

def test_enter_key():
    """Testet, welches Zeichen die Enter-Taste sendet."""
    print("Drücke eine Taste (besonders die Enter-Taste), um sie zu testen...")

    if os.name == "nt":  # Windows
        while True:
            char = msvcrt.getch()
            print(f"Eingegebenes Zeichen: {char}")  # Zeigt das Byte der gedrückten Taste
            if char in {b"\r", b"\n"}:
                print("✅ Enter-Taste erkannt!")
                break
    else:  # Linux/macOS
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in {"\n", "\r"}:  # Enter-Taste gedrückt
                    break
                elif char == "\x7f":  # Backspace-Taste
                    if password:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)  # Zeichen löschen
                elif char.isprintable():  # Zeichen hinzufügen, wenn es druckbar ist
                    password += char
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        print()  # Neue Zeile nach Eingabe
        return password