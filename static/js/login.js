document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const googleBtn = document.getElementById("googleLogin");

  // Login normal via backend Flask
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value.trim();
      const senha = document.getElementById("senha").value;

      const resp = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });

      const data = await resp.json();
      if (data.success) {
        window.location.href = data.redirect_url;
      } else {
        alert(data.message || "Erro ao fazer login.");
      }
    });
  }

  // Login com Google (via Supabase OAuth)
  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo: window.location.origin + "/api/set_token" },
      });

      if (error) {
        console.error("Erro no login Google:", error.message);
        alert("Erro ao entrar com o Google.");
      }
    });
  }
});
