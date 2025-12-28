from app.services import color_to_ass

def test_colors():
    test_cases = [
        ("red", "&H000000FF"),
        ("white", "&H00FFFFFF"),
        ("#FF0000", "&H000000FF"),
        ("#00FF00", "&H0000FF00"),
        ("#0000FF", "&H00FF0000"),
        ("0000FF", "&H00FF0000"),
    ]
    
    for input_color, expected in test_cases:
        result = color_to_ass(input_color)
        print(f"Input: {input_color} -> Result: {result} (Expected: {expected})")
        assert result == expected

if __name__ == "__main__":
    try:
        test_colors()
        print("All tests passed!")
    except AssertionError as e:
        print(f"Test failed!")
    except Exception as e:
        print(f"Error: {e}")
