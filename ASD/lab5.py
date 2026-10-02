# Реализовать алгоритм Бойера-Мура для поиска по образцу

def bad_character_table(pattern): # строит словарь, где для каждого символа образца хранится индекс его последнего вхождения
    table = {}
    m = len(pattern)
    for i in range(m):
        table[pattern[i]] = i
    return table

def good_suffix_table(pattern):
    m = len(pattern)
    table = [m] * (m + 1)  # по умолчанию сдвиг на всю длину образца
    
    for i in range(m - 1, -1, -1):
        suffix = pattern[i + 1:]  # хороший суффикс (совпавшая часть)
        if len(suffix) == 0:
            table[i] = 1
            continue
        
        found = False
        # Случай 1: ищем такое же вхождение суффикса в образце левее позиции i
        for k in range(i - 1, -1, -1):
            if pattern[k:k + len(suffix)] == suffix:
                table[i] = i - k
                found = True
                break
        
        # Случай 2: ищем префикс образца, совпадающий с суффиксом суффикса
        if not found:
            for k in range(1, len(suffix)):
                if pattern[:k] == suffix[-k:]:
                    table[i] = m - k
                    found = True
                    break
        
        # Случай 3: ничего не нашли — сдвигаем на всю длину
        if not found:
            table[i] = m
    
    return table

def boyer_moore_matcher(text, pattern):
    n = len(text)
    m = len(pattern)
    bad_char = bad_character_table(pattern)
    good_suffix = good_suffix_table(pattern)
    occurrences = []
    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            occurrences.append(shift)
            shift += good_suffix[0]
        else:
            bc_shift = j - bad_char.get(text[shift + j], -1)
            gs_shift = good_suffix[j + 1]
            shift += max(bc_shift, gs_shift)
    return occurrences

text = "ababcababacababa"
pattern = "ababa"
occurrences = boyer_moore_matcher(text, pattern)
print(f"Образец найден на позициях: {occurrences}")