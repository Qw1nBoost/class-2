<?php
$str = 'alb2c3';
$result = preg_replace_callback('/\d+/', function($matches) {
    $number = (int)$matches[0];
    return $number % 3;
}, $str);
echo $result;
?>
