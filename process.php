<?php
session_start();
if (!isset($_SESSION['logged_in'])) {
    header('Location: auth.php');
    exit;
}

// Sauvegarde des données
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = htmlspecialchars($_POST['title']);
    $message = htmlspecialchars($_POST['message']);

    // Simule une base de données (fichier JSON)
    file_put_contents('data.json', json_encode(['title' => $title, 'message' => $message]));
}

header('Location: admin.php');
exit;
?>
