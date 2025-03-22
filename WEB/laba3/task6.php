<?php

$a = 10;
$b = 3;
$remainder = $a % $b;
echo "Остаток от деления $a на $b: $remainder\n";

$a = 10;
$b = 3;
if ($a % $b == 0) {
    echo "Делится: " . ($a / $b) . "\n";
} else {
    echo "Делится с остатком: " . ($a % $b) . "\n";
}

$st = pow(2, 10);
echo "2 в 10 степени: $st\n";

$sqrt245 = sqrt(245);
echo "Квадратный корень из 245: $sqrt245\n";

$array = [4, 2, 5, 19, 13, 0, 10];
$sumOfSquares = 0;
foreach ($array as $value) {
    $sumOfSquares += $value * $value;
}
$sqrtSum = sqrt($sumOfSquares);
echo "Корень из суммы квадратов элементов массива: $sqrtSum\n";

$sqrt379 = sqrt(379);
echo "Квадратный корень из 379:\n";
echo "До целых: " . round($sqrt379) . "\n";
echo "До десятых: " . round($sqrt379, 1) . "\n";
echo "До сотых: " . round($sqrt379, 2) . "\n";

$sqrt587 = sqrt(587);
$rounded = [
    'floor' => floor($sqrt587),
    'ceil' => ceil($sqrt587)
];
echo "Квадратный корень из 587:\n";
echo "Округление в меньшую сторону: " . $rounded['floor'] . "\n";
echo "Округление в большую сторону: " . $rounded['ceil'] . "\n";

$numbers = [4, -2, 5, 19, -130, 0, 10];
$min = min($numbers);
$max = max($numbers);
echo "Минимальное число: $min\n";
echo "Максимальное число: $max\n";

$randomNumber = rand(1, 100);
echo "Случайное число от 1 до 100: $randomNumber\n";

$randomArray = [];
for ($i = 0; $i < 10; $i++) {
    $randomArray[] = rand(1, 100);
}
echo "Массив из 10 случайных чисел: " . implode(', ', $randomArray) . "\n";

$a = 15;
$b = 7;
$absDiff = abs($a - $b);
echo "Модуль разности $a и $b: $absDiff\n";

$array = [1, 2, -1, -2, 3, -3];
$positiveArray = array_map('abs', $array);
echo "Массив с положительными числами: " . implode(', ', $positiveArray) . "\n";

$number = 30;
$divisors = [];
for ($i = 1; $i <= $number; $i++) {
    if ($number % $i == 0) {
        $divisors[] = $i;
    }
}
echo "Делители числа $number: " . implode(', ', $divisors) . "\n";

$array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
$sum = 0;
$count = 0;
foreach ($array as $value) {
    $sum += $value;
    $count++;
    if ($sum > 10) {
        break;
    }
}
echo "Нужно сложить $count первых элементов, чтобы сумма была больше 10\n";
