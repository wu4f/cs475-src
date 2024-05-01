# Adds three numbers together and returns the result
def addition(number1, number2):
  result = number1 + number2
  return result

# Calculates the sum of the areas of two squares of lengths length1 and length2
def area(length1, length2):
  result = addition(length1*length1,length2*length2)
  return result

print(area(4,5))
