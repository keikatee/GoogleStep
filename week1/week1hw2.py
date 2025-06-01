from collections import Counter

# スコアテーブル（a〜z）
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2,
          1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]


def calculate_score(word: str) -> int:
    return sum(SCORES[ord(c) - ord('a')] for c in word)


def read_words(filepath: str) -> list[str]:
    with open(filepath) as f:
        return [line.strip() for line in f if line.strip()]


def preprocess_dictionary(dictionary: list[str]) -> list[tuple[int, str, Counter]]:
    processed = []
    for word in dictionary:
        score = calculate_score(word)
        counter = Counter(word)
        processed.append((score, word, counter))
    return sorted(processed, reverse=True)#（スコア,word,word count)のTuoleを作りスコア順に並べる


def anagram2_solution(random_word: str, dictionary: list[str]) -> tuple:
    input_counter = Counter(random_word)

    for score, word, word_counter in dictionary:
        if all(word_counter[c] <= input_counter.get(c, 0) for c in word_counter):
            return word, score  # ← 最初に作れる単語を見つけたら即 return
    return "", 0


def main(input_file: str, dictionary_file: str, output_file: str):
    dictionary = read_words(dictionary_file)
    input_words = read_words(input_file)

    processed_dictionary = preprocess_dictionary(dictionary)

    total_score = 0
    with open(output_file, "w") as fout:
        for input_word in input_words:
            best_word, score = anagram2_solution(input_word, processed_dictionary)
            total_score += score
            fout.write(best_word + "\n")
            print(f"{input_word} → {best_word} (Score: {score})")

    print("Total Score:", total_score)

if __name__ == "__main__":
    main("large.txt", "words.txt", "large_answer.txt")
#small, medium, largeそれぞれに合わせてコードを変更する

