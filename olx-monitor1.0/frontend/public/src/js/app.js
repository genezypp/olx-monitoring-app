document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Zapobiega odœwie¿eniu strony

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById("response-message").innerHTML =
                `<div class="alert alert-success">Login successful! Token: ${result.access_token}</div>`;
        } else {
            document.getElementById("response-message").innerHTML =
                `<div class="alert alert-danger">Error: ${result.detail}</div>`;
        }
    } catch (error) {
        document.getElementById("response-message").innerHTML =
            `<div class="alert alert-danger">Connection error: ${error.message}</div>`;
    }
});
