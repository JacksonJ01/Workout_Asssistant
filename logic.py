# 2 + 3 + 5

while True:
    reset = False
    userInput = input("Type Expression:"
                      "\n>>>").lower()
    userInput = userInput.split() if userInput not in "quit" else quit()
    lastDigit = False
    while lastDigit is False and reset is False:
        for num, x in enumerate(userInput):
            try:
                if int(x):
                    if (num + 1) % 3 == 0:
                        leftNum = int(userInput[num - 2])
                        operand = userInput[num - 1]
                        rightNum = int(userInput[num])
                        # print(leftNum, operand, rightNum)

                        userInput = userInput[:0] + userInput[3:]
                        total = 0
                        if operand == "+":
                            total = leftNum + rightNum
                        elif operand == "-":
                            total = leftNum - rightNum
                        elif operand == "*":
                            total = leftNum * rightNum
                        elif operand == "**":
                            total = leftNum ** rightNum
                        elif operand == "/":
                            total = leftNum / rightNum
                        elif operand == "//":
                            total = leftNum // rightNum
                        else:
                            raise TypeError

                        userInput.insert(0, str(total))
                        print(userInput)
                        if len(userInput) == 1:
                            lastDigit = True

            except ValueError:
                pass
            except TypeError:
                reset = True
                break

    try:
        print(userInput[0])
        print()
    except IndexError:
        pass