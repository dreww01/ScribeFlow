from app.services import color_to_ass

tests = [
    ("#FFFFFF", "&H00FFFFFF"),
    ("#000000", "&H00000000"),
    ("#FF0000", "&H000000FF"), # Red (RGB FF0000 -> BGR 0000FF)
    ("red", "&H000000FF"),
    ("blue", "&H00FF0000"),
    ("#FFF", "&H00FFFFFF"),
    ("invalid", "&H00FFFFFF"),
    ("orange", "&H0000A5FF"), # Orange (RGB FFA500 -> BGR 00A5FF)
]

print("Starting Color Conversion Tests...")
all_passed = True
for inp, expected in tests:
    res = color_to_ass(inp)
    status = "PASS" if res == expected else f"FAIL (Expected {expected})"
    if res != expected:
        all_passed = False
    print(f"Input: {inp:10} | Result: {res:12} | Status: {status}")

if all_passed:
    print("\nAll tests passed successfully!")
else:
    print("\nSome tests failed.")
