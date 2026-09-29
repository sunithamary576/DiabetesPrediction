const form = document.getElementById("loginForm");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    document.getElementById("message").textContent = data.message;
});