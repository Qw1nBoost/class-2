# 13.Решить задачу о раскладке по ящикам
# Есть N предметов заданного веса и ящики вместимостью C.Нужно разложить предметы по ящикам так,
# чтобы использовать минимальное количество ящиков. Порядок предметов не важен.

def min_boxes_greedy(items, capacity):
    """
    items: список весов предметов
    capacity: вместимость одного ящика
    """
    # Сортируем по убыванию: сначала кладем самые большие предметы
    items.sort(reverse=True)
    boxes = [] # Список текущих заполнений ящиков
    
    for item in items:
        if item > capacity:
            raise ValueError("Предмет больше вместимости ящика!")
            
        placed = False
        # Ищем первый ящик, куда влезет предмет
        for i in range(len(boxes)):
            if boxes[i] + item <= capacity:
                boxes[i] += item
                placed = True
                break
        
        # Если ни в один ящик не влез, берем новый
        if not placed:
            boxes.append(item)
            
    return len(boxes)

if __name__ == "__main__":
    items = [4, 8, 1, 4, 2, 1]
    capacity = 10
    print(f"Минимум ящиков: {min_boxes_greedy(items, capacity)}") # Ожидается 2