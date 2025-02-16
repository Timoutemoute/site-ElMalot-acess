document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.querySelector('.menu-icon');
    const navUl = document.querySelector('nav ul');

    menuIcon.addEventListener('click', function() {
        navUl.classList.toggle('active');
    });

    // Charger les propriétés
    fetch('/api/properties')
        .then(response => response.json())
        .then(data => {
            const propertiesDiv = document.getElementById('properties');
            data.forEach(property => {
                const propertyDiv = document.createElement('div');
                propertyDiv.className = 'property';
                propertyDiv.innerHTML = `
                    <h2>${property.title}</h2>
                    <p>${property.description}</p>
                    <p>Prix: ${property.price} €</p>
                `;
                propertiesDiv.appendChild(propertyDiv);
            });
        });
});

function addProperty() {
    // Logique pour ajouter une propriété
}

function editProperty() {
    // Logique pour modifier une propriété
}

function deleteProperty() {
    // Logique pour supprimer une propriété
}