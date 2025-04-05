<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $_SESSION['game'] = $_POST['game'] ?? '';
    $_SESSION['platform'] = $_POST['platform'] ?? '';
    $_SESSION['rating'] = $_POST['rating'] ?? '';

    header("Location: display.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Форма ввода</title>
</head>
<body>
    <h2>Введите ваши данные</h2>
    <form method="post">
        <label>Название игры: <input type="text" name="game" required></label><br><br>
        <label>Платформа: <input type="text" name="platform" required></label><br><br>
        <label>Рейтинг: <input type="date" name="rating" required></label><br><br>
        <button type="submit">Сохранить</button>
    </form>
</body>
</html>
