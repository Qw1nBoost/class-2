<?php

$numLanguages = 4; // кол-во языков которые знает Мэг
$months = 11;

$days = $months * 16;
$daysPerLanguage = $days / $numLanguages;

echo "Среднее количество дней на изучение одного языка: " . $daysPerLanguage;
