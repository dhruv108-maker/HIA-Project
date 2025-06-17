function toggleForms() {
    const loginSection = document.getElementById('login-section');
    const signinSection = document.getElementById('signin-section');

    // Toggle visibility
    if (loginSection.style.display === 'none') {
        loginSection.style.display = 'block';
        signinSection.style.display = 'none';
    } else {
        loginSection.style.display = 'none';
        signinSection.style.display = 'block';
    }
}



// Function to show content after successful login or signup
function showContent(username) {
    const loginSection = document.getElementById('login-section');
    const signinSection = document.getElementById('signin-section');
    const contentSection = document.getElementById('content-section');

    loginSection.style.display = 'none';
    signinSection.style.display = 'none';
    contentSection.style.display = 'block';
    document.querySelector("#content-section h1").textContent = `Welcome, ${username}!`;
}

// Example success logic after login or signup
function onLoginSuccess(username) {
    showContent(username);
}

function onSigninSuccess(username) {
    showContent(username);
}


//togle action

function toggleDiv(divId) {
    var element = document.getElementById(divId);

    // Toggle the 'active' class on the clicked div
    if (element.classList.contains('active')) {
        element.classList.remove('active');
    } else {
        element.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const equipmentDivs = document.querySelectorAll('.equipments');
    equipmentDivs.forEach(equipment => {
        equipment.addEventListener('click', function () {
            const equipmentName = this.getAttribute('data-equipment-name');
            const equipmentDescription = this.getAttribute('data-equipment-description');

            const equipmentTitle = document.getElementById('equipment-title');
            const equipmentDesc = document.getElementById('equipment-description');
            const equipmentImg = document.getElementById('equipment-image');

            // Debugging logs
            console.log(equipmentTitle); // Check if it's null
            console.log(equipmentDesc); // Check if it's null

            // Update the HTML content only if elements are found
            if (equipmentTitle && equipmentDesc) {
                equipmentTitle.innerText = equipmentName;
                equipmentDesc.innerText = equipmentDescription;
            } 
        });
    });
});


