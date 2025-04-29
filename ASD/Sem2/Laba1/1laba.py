def cross_product(o, a, b): # вычисляет векторное произведение, которое помогает определить ориентацию тройки точек
    return (a[0] - o[0])*(b[1] - o[1]) - (a[1] - o[1])*(b[0] - o[0])

def jarvis_march(points):
    n = len(points)
    if n < 3:
        return []  # Выпуклая оболочка не существует для менее чем 3 точек
    
    # Находим самую левую точку
    leftmost = min(points, key=lambda x: (x[0], x[1]))
    
    hull = []
    current_point = leftmost
    next_point = None
    
    while True:
        hull.append(current_point)
        next_point = points[0] if points[0] != current_point else points[1]
        
        for candidate in points:
            if candidate == current_point:
                continue
            cross = cross_product(current_point, next_point, candidate)
            if cross > 0 or (cross == 0 and 
               ((candidate[0] - current_point[0])**2 + (candidate[1] - current_point[1])**2 > 
                (next_point[0] - current_point[0])**2 + (next_point[1] - current_point[1])**2)):
                next_point = candidate
        
        current_point = next_point
        if current_point == hull[0]:
            break
    
    return hull

# Ввод точек
n = int(input("Введите количество точек: "))
points = []
for i in range(n):
    x, y = map(float, input(f"Введите координаты точки {i+1} (x y): ").split())
    points.append((x, y))

# Построение выпуклой оболочки
convex_hull = jarvis_march(points)

# Проверка существования выпуклой оболочки
if len(convex_hull) < 3:
    print("Выпуклая оболочка не существует (все точки коллинеарны или их меньше 3)")
else:
    print("Выпуклая оболочка существует и состоит из следующих точек:")
    for point in convex_hull:
        print(point)
