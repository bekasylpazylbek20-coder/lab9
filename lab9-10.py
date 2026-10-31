import heapq
import math
from collections import Counter
from itertools import count


def build_tree(freq):
    heap = []
    order = count()

    for char, f in sorted(freq.items()):
        heapq.heappush(heap, (f, next(order), char))

    if len(heap) == 1:
        return heap[0][2]

    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(order), (left, right)))

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


def calculate_metrics(freq, codes):
    total = sum(freq.values())
    probabilities = [f / total for f in freq.values()]

    H = -sum(p * math.log2(p) for p in probabilities)
    L = sum(freq[c] / total * len(codes[c]) for c in freq)

    efficiency = H / L if L else 0
    redundancy = 1 - efficiency

    return H, L, efficiency, redundancy


def main():
    text = (
        "Информационные технологии играют важную роль в современном мире. "
        "Люди используют компьютеры и интернет для учебы, работы и общения. "
        "Каждый день мы передаем большое количество информации через различные сети. "
        "Для экономии памяти и ускорения передачи данных применяются алгоритмы сжатия. "
        "Одним из таких методов является алгоритм Хаффмана, который позволяет "
        "создавать короткие коды для часто встречающихся символов."
    )

    freq = dict(Counter(text))
    tree = build_tree(freq)
    codes = get_codes(tree)

    bits = encode(text, codes)

    H, L, efficiency, redundancy = calculate_metrics(freq, codes)

    original_bytes = len(text.encode("utf-8"))
    compressed_bytes = (len(bits) + 7) // 8
    padding = (8 - len(bits) % 8) % 8

    # Таблица частот сохраняется в UTF-8.
    # На каждый символ: 1 байт длины + UTF-8 символ + 4 байта частоты.
    table_bytes = 2 + sum(
        1 + len(c.encode("utf-8")) + 4
        for c in freq
    )

    total_bytes = compressed_bytes + table_bytes

    print("Количество символов:", len(text))
    print("Уникальных символов:", len(freq))

    print("\nТаблица Хаффмана")
    print(f"{'Символ':<12}{'Частота':<12}{'Код'}")

    for char in sorted(freq):
        name = repr(char)
        print(f"{name:<12}{freq[char]:<12}{codes[char]}")

    print("\nХарактеристики:")
    print(f"Энтропия H(X): {H:.4f}")
    print(f"Средняя длина L: {L:.4f}")
    print(f"Эффективность: {efficiency * 100:.2f}%")
    print(f"Избыточность: {redundancy * 100:.2f}%")

    print("\nРазмеры:")
    print("Исходный UTF-8:", original_bytes, "байт")
    print("Битовый поток:", len(bits), "бит")
    print("Упакованные данные:", compressed_bytes, "байт")
    print("Выравнивание:", padding, "бит")
    print("Таблица частот:", table_bytes, "байт")
    print("Общий размер:", total_bytes, "байт")

    saving = (1 - total_bytes / original_bytes) * 100

    print(f"Экономия с учетом таблицы: {saving:.2f}%")

    if total_bytes < original_bytes:
        print("Вывод: сжатие выгодно.")
    else:
        print("Вывод: сжатие невыгодно из-за служебных данных.")


if __name__ == "__main__":
    main()