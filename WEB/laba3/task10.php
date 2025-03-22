<?php

function isSumGreaterThanTen($num1, $num2)
{
    return ($num1 + $num2) > 10;
}

echo isSumGreaterThanTen(5, 6) ? 'true' : 'false';
echo "\n";

function areNumbersEqual($num1, $num2)
{
    return $num1 == $num2;
}

echo areNumbersEqual(4, 4) ? 'true' : 'false';
echo "\n";

$test = 0;
if (($test == 0) echo 'верно');
echo "\n";

$age = 25; // Пример значения
if ($age < 10 || $age > 99)
{
    echo "Число меньше 10 или больше 99\n";
}
else
{
    $sum = array_sum(str_split((string)$age));
    if ($sum <= 9)
    {
        echo "Сумма цифр однозначна\n";
    }
    else
    {
        echo "Сумма цифр двузначна\n";
    }
}

$arr = [1, 2, 3]; // Пример массива
if (count($arr) == 3) {
    echo "Сумма элементов массива: " . array_sum($arr) . "\n";
}
