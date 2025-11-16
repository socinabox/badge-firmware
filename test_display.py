#!/usr/bin/env python3
"""
Display Testing - Find display limits and capabilities
Author: David Broggy
"""

import sys
import time

def main():
    print("=" * 50)
    print("DISPLAY LIMITS TEST")
    print("=" * 50)

    from freewili.fw import FreeWili

    result = FreeWili.find_first()
    if result.is_err():
        print("✗ No badge found")
        return 1

    badge = result.unwrap()
    print("✓ Badge connected\n")

    tests = [
        ("Test 1: Single short line", "Hello World"),

        ("Test 2: Multiple short lines", "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"),

        ("Test 3: Long single line", "This is a very long line to test horizontal limits and wrapping behavior"),

        ("Test 4: Many lines", "\n".join([f"Line {i}" for i in range(1, 20)])),

        ("Test 5: Mixed content", "MVP SUMMIT\n2026\nSecurity Badge\nTest Display\nMore Text\nEven More\nAnd More"),

        ("Test 6: Simple message", "MVP\nSummit\n2026"),
    ]

    for i, (description, text) in enumerate(tests, 1):
        print(f"\n[Test {i}/6] {description}")
        print(f"Text length: {len(text)} chars")
        print(f"Lines: {text.count(chr(10)) + 1}")

        result = badge.show_text_display(text)

        if result.is_ok():
            print("✓ Displayed")
            print("\nLook at badge screen now!")
            input("Press Enter when ready for next test...")
        else:
            print(f"✗ Failed: {result.unwrap_err()}")
            return 1

    print("\n" + "=" * 50)
    print("TESTS COMPLETE")
    print("=" * 50)
    return 0

if __name__ == "__main__":
    sys.exit(main())
