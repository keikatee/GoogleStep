#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiplication(line, index):
    token = {'type': 'MULTIPLICATION'}
    return token, index + 1


def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_multi_div(tokens):
    """Evaluate the calculation of multiplication and division."""
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLICATION':#index - 1が'MULTIPLICATION'だった場合
                if tokens[index - 2]['type'] == 'NUMBER':#index - 2が'NUMBER'だった場合
                    answer = tokens[index - 2]['number'] * tokens[index]['number']
                    tokens = (
                        tokens[: index - 2]
                        + [{"type": "NUMBER", "number": answer}]
                        + tokens[index + 1:]
                    )#tokensの中身を掛け算したものに変更
                    index -= 2
                else:
                    print('Invalid syntax')
                    exit(1)
            elif tokens[index - 1]['type'] == 'DIVISION':#index - 1が'DIVISION'だった場合
                if tokens[index - 2]['type'] == 'NUMBER':# index - 2が'NUMBER'だった場合
                    answer = tokens[index - 2]['number'] / tokens[index]['number']
                    tokens = (
                            tokens[: index - 2]
                            + [{"type": "NUMBER", "number": answer}]
                            + tokens[index + 1:]
                    )  # tokensの中身を割り算したものに変更
                    index -= 2
                else:
                    print('Invalid syntax')
                    exit(1)
        index += 1
    return tokens


def evaluate(tokens):
    tokens = evaluate_multi_div(tokens)

    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0+2")
    test("1.0+2.0")
    test("1+2*4") #check if multiplication is correct
    test("1.0+2*3.0")
    test("1*0.1+20*3.0")
    test("50+40/2")#check if division is correct
    test("1.0+2/3.0")
    test("20/2.0+60/3.0")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
