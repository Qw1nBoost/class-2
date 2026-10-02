# ввести N точек своими координатами (x,y). Затем требуется определить,
# существует ли выпуклая оболочка заданного множества точек.

# ГРЭХЕМА
import math

def orientation(p, q, r):
    # 1. Исправлена формула векторного произведения (q-p) x (r-p)
    val = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    if val == 0:
        return 0
    return 1 if val > 0 else -1

def convex_hull(points):
    if len(points) < 3:
        return None
    
    # 2. Находим самую нижнюю точку (если их несколько, то самую левую)
    p0 = min(points, key=lambda p: (p[1], p[0]))
    
    # 3. Сортируем остальные точки по полярному углу относительно p0
    # Если углы совпадают, сортируем по расстоянию от p0
    def sort_key(p):
        angle = math.atan2(p[1] - p0[1], p[0] - p0[0])
        dist = (p[0] - p0[0])**2 + (p[1] - p0[1])**2
        return (angle, dist)
        
    points.remove(p0)
    points.sort(key=sort_key)
    
    hull = [p0]
    for point in points:
        # 4. Оставляем только строгие левые повороты (orientation == 1)
        while len(hull) > 1 and orientation(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
        
    return hull

N = int(input("Введите количество точек: "))
points = []
for _ in range(N):
    x, y = map(int, input("Введите координаты точки (x y): ").split())
    points.append((x, y))

hull = convex_hull(points)
if hull:
    print("Выпуклая оболочка существует. Точки выпуклой оболочки:")
    for point in hull:
        print(point)
else:
    print("Выпуклая оболочка не существует.")