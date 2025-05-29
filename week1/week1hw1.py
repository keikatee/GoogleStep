def solution(random_word, dictionary):
    sorted_random_word = sorted_word(random_word)

    new_dictionary = []
    for word in dictionary:
        new_dictionary.append((sorted_word(word), word))
    sorted_dic = sorted(new_dictionary)

    anagram = binary_search(sorted_random_word, sorted_dic)
    return anagram


def sorted_word(word):
    sorted_list = sorted(word)
    result = ''.join(sorted_list)
    return result


def binary_search(word, dic):
    high = len(dic) - 1
    low = 0
    anagramset = []

    while low <= high:
        mid = (high + low) // 2
        if dic[mid][0] == word:
            anagramset.append(dic[mid][1])

            # 左側の一致を探索
            before = mid - 1
            while before >= 0 and dic[before][0] == word:
                anagramset.append(dic[before][1])
                before -= 1

            # 右側の一致を探索
            after = mid + 1
            while after < len(dic) and dic[after][0] == word:
                anagramset.append(dic[after][1])
                after += 1

            return anagramset
        elif dic[mid][0] < word:
            low = mid + 1
        else:
            high = mid - 1

    return []


def load_dictionary(filepath):
    with open(filepath, 'r') as file:
        dictionary = [line.strip() for line in file if line.strip()]
    return dictionary


if __name__ == "__main__":
    # words.txt を読み込む
    dictionary = load_dictionary("words.txt")  # week1hw1.py と同じフォルダにある想定

    # 調べたい単語
    input_word = "darc"

    # アナグラム検索
    result = solution(input_word, dictionary)
    print(f"Anagrams of '{input_word}': {result}")
