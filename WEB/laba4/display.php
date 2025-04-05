<?php
session_start();
$game = $_SESSION['game'] ?? 'Не задано';
$platform = $_SESSION['platform'] ?? 'Не задано';
$rating = $_SESSION['rating'] ?? 'Не задано';
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ваши данные</title>
</head>
<body>
    <h2>Ваши данные</h2>
    <p><strong>Название игры:</strong> <?php echo htmlspecialchars($game); ?></p>
    <p><strong>Платформа:</strong> <?php echo htmlspecialchars($platform); ?></p>
    <p><strong>Рейтинг:</strong> <?php echo htmlspecialchars($rating); ?></p>
    <a href="form.php">Назад к форме</a>
</body>
</html>
