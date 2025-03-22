<?php

$num = 17;
echo $num, " - целочисленная переменная\n";

$floatNumber = 1.17;
echo "\n{$floatNumber} - переменная с плавающей запятой\n";


echo "\n", (10 + 2), " - раньше это число не встречалось\n";

$lastMonth = 1500;
$thisMonth = 1200;

echo "\nНасколько больше я потратил в прошлом месяце, чем в этом месяце? ", abs($lastMonth - $thisMonth);
