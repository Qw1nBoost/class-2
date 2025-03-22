<?php

function increaseEnthusiasm($str)
{
    return $str . "!";
}

echo increaseEnthusiasm("Hello") . "\n";

function repeatThreeTimes($str)
{
    return $str . $str . $str;
}

echo repeatThreeTimes("Repeat3times ") . "\n";

echo increaseEnthusiasm(repeatThreeTimes("Наповторяли ")) . "\n";

function cut($str, $length = 10)
{
    return substr($str, 0, $length);
}

echo cut("Это длинная строка", 5) . "\n";
echo cut("Это длинная строка") . "\n";

function printArrayRecursively($array, $index = 0)
{
    if ($index < count($array))
    {
        echo $array[$index] . "\n";
        printArrayRecursively($array, $index + 1);
    }
}

$numbers = [1, 2, 3, 4, 5];
printArrayRecursively($numbers);

function sumDigits($number)
{
    while ($number > 9) {
        $number = array_sum(str_split((string)$number));
    }
    return $number;
}

$number = 12345;
echo "Сумма цифр числа $number: " . sumDigits($number) . "\n";
