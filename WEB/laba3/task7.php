<?php

function printStringReturnNumber()
{
    echo "Строка\n";
    return 263;
}

$my_num = printStringReturnNumber();

echo "Число: $my_num\n";
