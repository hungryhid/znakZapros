const API_URL = "http://127.0.0.1:8000";

const loginContainer = document.getElementById("login-form");
const registerContainer = document.getElementById("register-form");
const profileContainer = document.getElementById("profile");

const showRegisterButton = document.getElementById("show-register");
const showLoginButton = document.getElementById("show-login");

const loginForm = document.getElementById("login");
const registerForm = document.getElementById("register");

const loginError = document.getElementById("login-error");
const registerError = document.getElementById("register-error");

const logoutButton = document.getElementById("logout");

function showLogin() {
    loginContainer.classList.add("active");
    registerContainer.classList.remove("active");
    profileContainer.classList.remove("active");

    loginError.textContent = "";
    registerError.textContent = "";
}

function showRegister() {
    loginContainer.classList.remove("active");
    registerContainer.classList.add("active");
    profileContainer.classList.remove("active");

    loginError.textContent = "";
    registerError.textContent = "";
}

function showProfile(user) {
    loginContainer.classList.remove("active");
    registerContainer.classList.remove("active");
    profileContainer.classList.add("active");

    document.getElementById("profile-id").textContent = user.id;
    document.getElementById("profile-name").textContent = user.name;
    document.getElementById("profile-email").textContent = user.email;
    document.getElementById("profile-created").textContent = user.created_at;
}

showRegisterButton.addEventListener("click", showRegister);
showLoginButton.addEventListener("click", showLogin);


registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    registerError.textContent = "";

    const data = {
        name: document.getElementById("register-name").value,
        email: document.getElementById("register-email").value,
        password: document.getElementById("register-password").value
    };

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            registerError.textContent =
                result.detail ?? "Не удалось зарегистрироваться";

            return;
        }

        showLogin();

        document.getElementById("login-email").value = data.email;

    } catch (error) {
        registerError.textContent =
            "Не удалось подключиться к серверу";
    }
});


loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    loginError.textContent = "";

    const data = {
        email: document.getElementById("login-email").value,
        password: document.getElementById("login-password").value
    };

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            loginError.textContent =
                result.detail ?? "Неверный email или пароль";

            return;
        }

        const token = result.access_token;

        localStorage.setItem("access_token", token);

        await loadProfile();

    } catch (error) {
        loginError.textContent =
            "Не удалось подключиться к серверу";
    }
});


async function loadProfile() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        showLogin();
        return;
    }

    const response = await fetch(`${API_URL}/profile`, {
        method: "GET",

        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        localStorage.removeItem("access_token");
        showLogin();
        return;
    }

    const user = await response.json();

    showProfile(user);
}


logoutButton.addEventListener("click", () => {
    localStorage.removeItem("access_token");

    showLogin();
});


window.addEventListener("DOMContentLoaded", () => {
    loadProfile();
});