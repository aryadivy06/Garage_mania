// service_forget.js

function requestSPOtp() {
    const identifier = document.getElementById("identifier").value;

    fetch("/send-sp-otp/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify({ identifier }),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            document.getElementById("otp-section").classList.remove("hidden");
        }
    });
}

function verifySPOtp() {
    const otp = document.getElementById("otp").value;

    fetch("/verify-sp-otp/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify({ otp }),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            document.getElementById("password-section").classList.remove("hidden");
            document.getElementById("submit-btn").classList.remove("hidden");
        }
    });
}

document.getElementById("spForgetForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const password1 = document.getElementById("password1").value;
    const password2 = document.getElementById("password2").value;

    fetch("/reset-sp-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify({ password1, password2 }),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            window.location.href = "/service_provider_login/";
        }
    });
});
