document.addEventListener("DOMContentLoaded", function () {
    fetch("/get_users")
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;  // Redirect immediately
                throw new Error("Redirecting...");  // Stop execution
            }
            return response.json();
        })
        .then(users => {
            if (!users) return;  // Stop execution if redirected

            const tbody = document.querySelector("#usersTable tbody");
            tbody.innerHTML = ""; // Clear existing data

            users.forEach(user => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.role}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error("Error loading users:", error));
});
