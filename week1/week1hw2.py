from collections import Counter

# スコアテーブル（a〜z）
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2,
          1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]


def calculate_score(word: str) -> int:
    return sum(SCORES[ord(c) - ord('a')] for c in word)


def read_words(filepath: str) -> list[str]:
    with open(filepath) as f:
        return [line.strip() for line in f if line.strip()]


def anagram2_solution(random_word: str, dictionary: list[str]) -> str:
    input_counter = Counter(random_word)
    max_score = 0
    best_word = ""

    for word in dictionary:
        word_counter = Counter(word)
        if all(word_counter[c] <= input_counter.get(c, 0) for c in word_counter):
            score = calculate_score(word)
            if score > max_score:
                max_score = score
                best_word = word

    return best_word


def main(input_file: str, dictionary_file: str, output_file: str):
    dictionary = read_words(dictionary_file)
    input_words = read_words(input_file)

    total_score = 0
    with open(output_file, "w") as fout:
        for input_word in input_words:
            best_word = anagram2_solution(input_word, dictionary)
            score = calculate_score(best_word)
            total_score += score
            fout.write(best_word + "\n")
            print(f"{input_word} → {best_word} (Score: {score})")

    print("Total Score:", total_score)


if __name__ == "__main__":
    main("small.txt", "words.txt", "small_answer.txt")
#small, medium, largeそれぞれに合わせてコードを変更する
