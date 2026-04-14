def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b

print("=== Persistent Calculator ===")
print("Examples: 1+2 | 11*12 | 1 - 3 | 4/1")
print("Type 'exit' to stop.\n")

while True:
    expr = input("Enter Values: ")

    if expr.lower() == "exit":
        print("Calculator stopped.")
        break

    try:
        # Remove all spaces
        expr = expr.replace(" ", "")

        # Find operator
        for op in ["+", "-", "*", "/"]:
            if op in expr:
                num1, num2 = expr.split(op, 1)
                operator = op
                break
        else:
            print("Invalid expression\n")
            continue

        num1 = float(num1)
        num2 = float(num2)

        match operator:
            case "+":
                result = add(num1, num2)
            case "-":
                result = subtract(num1, num2)
            case "*":
                result = multiply(num1, num2)
            case "/":
                result = divide(num1, num2)
            
        print(f"Result: {result}\n")

    except ZeroDivisionError:
        print("Error: Division by zero\n")

    except ValueError:
        print("Invalid input\n")
