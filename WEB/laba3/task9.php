<?php

$array = [];
for ($i = 1; $i <= 5; $i++)
{
    $array[] = str_repeat('x', $i);
}
print_r($array);

function arrayFill($value, $count)
{
    return array_fill(0, $count, $value);
}

$filledArray = arrayFill('x', 5);
print_r($filledArray);

$twoDimensionalArray = [[1, 2, 3], [4, 5], [6]];
$sum = 0;
foreach ($twoDimensionalArray as $subArray)
{
    $sum += array_sum($subArray);
}
echo "Сумма элементов двухмерного массива: $sum\n";

$matrix = [];
$value = 1;
for ($i = 0; $i < 3; $i++)
{
    for ($j = 0; $j < 3; $j++)
    {
        $matrix[$i][$j] = $value++;
    }
}
print_r($matrix);

$numbers = [2, 5, 3, 9];
$result = ($numbers[0] * $numbers[1]) + ($numbers[2] * $numbers[3]);
echo "Результат: $result\n";

$user = [
    'name' => 'Андрей',
    'surname' => 'Андреев',
    'patronymic' => 'Андреевич'
];
echo "ФИО: {$user['surname']} {$user['name']} {$user['patronymic']}\n";

$date = [
    'year' => date('Y'),
    'month' => date('m'),
    'day' => date('d')
];
echo "Дата: {$date['year']}-{$date['month']}-{$date['day']}\n";

$arr = ['a', 'b', 'c', 'd', 'e'];
echo "Количество элементов в массиве: " . count($arr) . "\n";
echo "Последний эллемент массива: ", end($arr) . "\n";
echo "Предпоследний элемент массива: ", prev($arr) . "\n";
