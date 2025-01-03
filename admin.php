<?php
session_start();

// Authentification simplifiée
if (!isset($_SESSION['logged_in'])) {
    header('Location: auth.php');
    exit;
}

// Traitement de la personnalisation
$title = $_POST['title'] ?? 'Bienvenue sur mon site';
$message = $_POST['message'] ?? 'Ceci est une page personnalisable depuis l\'espace administrateur';
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Espace Administrateur</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Espace Administrateur</h1>
    </header>
    <main>
        <form action="process.php" method="POST">
            <label for="title">Titre du site :</label>
            <input type="text" id="title" name="title" value="<?= htmlspecialchars($title) ?>" required>
            
            <label for="message">Message principal :</label>
            <textarea id="message" name="message" required><?= htmlspecialchars($message) ?></textarea>
            
            <button type="submit">Enregistrer</button>
        </form>
    </main>
    <footer>
        <a href="index.html">Retour au site</a>
    </footer>
</body>
</html>
