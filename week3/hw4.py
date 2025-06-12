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


def read_right_parentheses(line, index):
    token = {'type': 'RIGHTPARE'}
    return token, index + 1


def read_left_parentheses(line, index):
    token = {'type': 'LEFTPARE'}
    return token, index + 1


def read_abs(line, index):
    if line[index:index+3] == 'abs':
        return {'type': 'ABS'}, index + 3
    else:
        print('Invalid function name starting with "a"')
        exit(1)


def read_int(line, index):
    if line[index:index+3] == 'int':
        return {'type': 'INT'}, index + 3
    else:
        print('Invalid function name starting with "i"')
        exit(1)


def read_round(line, index):
    if line[index:index+5] == 'round':
        return {'type': 'ROUND'}, index + 5
    else:
        print('Invalid function name starting with "r"')
        exit(1)


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
        elif line[index] == ')':
            (token, index) = read_right_parentheses(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parentheses(line, index)
        elif line[index] == 'a':
            (token, index) = read_abs(line, index)
        elif line[index] == 'i':
            (token, index) = read_int(line, index)
        elif line[index] == 'r':
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_function_calls(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] in ('ABS', 'INT', 'ROUND'):
            if tokens[index + 1]['type'] == 'LEFTPARE':
                # 関数の引数（括弧内）を探す
                index_left = index + 1
                index_right = index_left + 1
                depth = 1
                while index_right < len(tokens):
                    if tokens[index_right]['type'] == 'LEFTPARE':
                        depth += 1
                    elif tokens[index_right]['type'] == 'RIGHTPARE':
                        depth -= 1
                        if depth == 0:
                            break
                    index_right += 1
                if depth != 0:
                    print("Mismatched parentheses in function call")
                    exit(1)

                # 括弧内のトークンを評価
                inner_tokens = tokens[index_left + 1: index_right]
                value = evaluate(inner_tokens)

                if tokens[index]['type'] == 'ABS':
                    value = abs(value)
                elif tokens[index]['type'] == 'INT':
                    value = int(value)
                elif tokens[index]['type'] == 'ROUND':
                    value = round(value)

                # トークンの置き換え
                tokens = (
                    tokens[:index] +
                    [{'type': 'NUMBER', 'number': value}] +
                    tokens[index_right + 1:]
                )
                index = 0  # 戻って再探索
                continue
        index += 1
    return tokens


def evaluate_parentheses(tokens):
    """Evaluate the calculations for the portion in parentheses."""
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'RIGHTPARE':
            index_left = index - 1
            while index_left >= 0:
                if tokens[index_left]['type'] == 'LEFTPARE':
                    break
                else:
                    index_left -= 1
            part_tokens = tokens[index_left + 1: index]#括弧内のtokens
            eva_part_tokens = evaluate(part_tokens)#括弧内のtokensの中身を求める
            tokens = (
                    tokens[: index_left]
                    + [{"type": "NUMBER", "number": eva_part_tokens}]
                    + tokens[index + 1:]
            )  # 括弧内のtokensの中身をtokens全体に反映させる
            index = index_left + 1#indexの位置をindex_left+1にし確認していない括弧を確認できるようにセットする
        else:
            index += 1
    return tokens


def evaluate_multi_div(tokens):
    """Evaluate the multiplication and division calculations."""
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
    tokens = evaluate_function_calls(tokens)
    tokens = evaluate_parentheses(tokens)
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
    test("3*(3+5)")#check if the evaluate_parentheses works
    test("3*(24/(3+5))")
    test("3*(24/(3+5))+3")
    test("3.1*(24/(3-5))-20.1")
    test("abs(2.4)")#check if the abs function works
    test("int(3.5)")#check if the int function works
    test("round(2.7)")#check if the round function works
    test("abs(int(2.5)*(-8))")
    test("round(4.8)/2+8.5")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
