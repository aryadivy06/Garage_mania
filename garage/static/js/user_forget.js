function getCSRFToken() {
  let csrfToken = null;
  let cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    let c = cookie.trim();
    if (c.startsWith("csrftoken=")) {
      csrfToken = c.substring("csrftoken=".length, c.length);
      break;
    }
  }
  return csrfToken;
}

// Request OTP
function requestOTP() {
  let identifier = document.getElementById("identifier").value;

  fetch("/send-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ identifier: identifier }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(data.message);
        document.getElementById("otp-section").classList.remove("hidden");
      } else {
        alert(data.message || "Failed to send OTP.");
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Verify OTP
function verifyOTP() {
  let otp = document.getElementById("otp").value;

  fetch("/verify-otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ otp: otp }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(data.message);
        document.getElementById("password-section").classList.remove("hidden");
        document.getElementById("submit-btn").classList.remove("hidden");
      } else {
        alert(data.message || "OTP verification failed.");
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Submit new password
document.getElementById("forgetForm").addEventListener("submit", function (e) {
  e.preventDefault();

  let password1 = document.getElementById("password1").value;
  let password2 = document.getElementById("password2").value;

  fetch("/reset-password/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ password1: password1, password2: password2 }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(data.message);
        window.location.href = "/login/";
      } else {
        alert(data.message || "Failed to reset password.");
      }
    })
    .catch((error) => console.error("Error:", error));
});
