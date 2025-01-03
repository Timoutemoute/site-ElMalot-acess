<?php
// Inclure le fichier de configuration
require_once 'config.php';

// Déterminer la page à afficher
$page = isset($_GET['page']) ? $_GET['page'] : 'home';
$pagePath = "pages/$page.php";

if (!file_exists($pagePath)) {
    $pagePath = "pages/home.php"; // Page par défaut
}

include 'includes/header.php'; // En-tête
include $pagePath;             // Contenu principal
include 'includes/footer.php'; // Pied de page
?>
