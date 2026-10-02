# Реализовать алгоритм поиска по образцу с помощью конечного автомата

def zagotovka(pattern, alphabet): # создает таблицу переходов для конечного автомата
    # есть m + 1 состояние (от 0 до m, m — длина образца)
    # Состояние state означает, что мы успешно распознали префикс образца длиной state.
    # Состояние m — финальное (успешное) состояние, означающее, что весь образец найден.
    m = len(pattern)
    transition_table = [{} for _ in range(m + 1)] # Каждый словарь описывает, в какое состояние мы перейдем из текущего, если увидим определенный символ
    for state in range(m + 1):
        for char in alphabet:
            next_state = min(m, state + 1)
            while next_state > 0 and pattern[:next_state] != (pattern[:state] + char)[-next_state:]:
                next_state -= 1
            transition_table[state][char] = next_state
    return transition_table

def obraz(text, pattern, alphabet):
    n = len(text)
    m = len(pattern)
    transition_table = zagotovka(pattern, alphabet)
    state = 0
    occurrences = []
    for i in range(n):
        if text[i] in transition_table[state]:
            state = transition_table[state][text[i]]
        else:
            state = 0
        if state == m:
            occurrences.append(i - m + 1)
    return occurrences

text = "ababca  babacab"
pattern = "ab"
alphabet = {'a', 'b', 'c'}
occurrences = obraz(text, pattern, alphabet)
print(f"Образец найден на позициях: {occurrences}")