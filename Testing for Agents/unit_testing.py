import unittest

# Example tool
def calculator_tool(expr):
    try:
        return str(eval(expr))
    except:
        return "Invalid expression."

class TestTools(unittest.TestCase):
    def test_calculator(self):
        self.assertEqual(calculator_tool("2 + 3"), "5")
        self.assertEqual(calculator_tool("10 * 2"), "20")
        self.assertEqual(calculator_tool("invalid"), "Invalid expression.")

if __name__ == "__main__":
    unittest.main()
    