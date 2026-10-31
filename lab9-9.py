import heapq
import math
from collections import Counter
from itertools import count


def build_tree(freq):
    if not freq:
        raise ValueError("Словарь частот пуст")

    heap = []
    order = count()

    for char, f in sorted(freq.items()):
        if f <= 0:
            raise ValueError("Частоты должны быть положительными")
        heapq.heappush(heap, (f, next(order), char))

    if len(heap) == 1:
        return heap[0][2]

    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)

        heapq.heappush(
            heap, (f1 + f2, next(order), (left, right))
        )

    return heap[0][2]


def get_codes(tree, code="", codes=None):
    if codes is None:
        codes = {}

    if isinstance(tree, str):
        codes[tree] = code or "0"
    else:
        get_codes(tree[0], code + "0", codes)
        get_codes(tree[1], code + "1", codes)

    return codes


def encode(text, codes):
    return "".join(codes[char] for char in text)


def decode(bits, tree):
    if isinstance(tree, str):
        if any(bit != "0" for bit in bits):
            raise ValueError("Некорректный код")
        return tree * len(bits)

    result = []
    node = tree

    for bit in bits:
        if bit not in "01":
            raise ValueError("Некорректный бит")

        node = node[0] if bit == "0" else node[1]

        if isinstance(node, str):
            result.append(node)
            node = tree

    if node != tree:
        raise ValueError("Неполный код")

    return "".join(result)


def calculate_metrics(freq, codes):
    total = sum(freq.values())

    probabilities = {
        char: f / total for char, f in freq.items()
    }

    L = sum(
        probabilities[char] * len(codes[char])
        for char in freq
    )

    H = -sum(
        p * math.log2(p)
        for p in probabilities.values()
    )

    eta = H / L if L > 0 else 1.0

    return probabilities, L, H, eta


def main():
    text = "ABCDE"
    freq = dict(Counter(text))

    tree = build_tree(freq)
    codes = get_codes(tree)

    probabilities, L, H, eta = calculate_metrics(freq, codes)

    print("Таблица кодов Хаффмана")
    print(f"{'Символ':<10}{'Частота':<10}{'Код':<10}")

    for char in sorted(freq):
        print(f"{char:<10}{freq[char]:<10}{codes[char]:<10}")

    print(f"\nL = {L:.4f}")
    print(f"H(X) = {H:.4f}")
    print(f"η = {eta:.4f}")

    encoded = encode(text, codes)
    decoded = decode(encoded, tree)

    print("\nИсходный текст:", text)
    print("Закодированный:", encoded)
    print("Декодированный:", decoded)
    print("Проверка:", decoded == text)

    single_freq = {"A": 5}
    single_tree = build_tree(single_freq)
    single_codes = get_codes(single_tree)

    print("\nОдин уникальный символ:")
    print("Код:", single_codes["A"])
    print("Результат:", encode("AAAAA", single_codes))


if __name__ == "__main__":
    main()