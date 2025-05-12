import { useState } from "react";
import { useRouter } from "next/router";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
  
    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          email: email,
          password: password,
        }),
        credentials: "include",
      });
  
      console.log("response.status", response.status);  
      console.log("response.headers", response.headers); 
  
      const data = await response.json().catch(err => {
        console.error("JSON parsing error:", err);
        return null;
      });
  
      console.log("data", data); 
  
      if (response.ok && data) {
        localStorage.setItem("access_token", data.access_token);
        router.push("/dashboard");
      } else {
        setError(data?.detail || "Login failed");
      }
    } catch (err) {
      console.error("fetch error:", err);
      setError("An error occurred. Try again.");
    }
  };  

  return (
    <div style={{ maxWidth: "400px", margin: "auto", paddingTop: "100px" }}>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ display: "block", marginBottom: "10px", width: "100%" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ display: "block", marginBottom: "10px", width: "100%" }}
        />
        <button type="submit" style={{ width: "100%" }}>
          Login
        </button>
      </form>
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
    </div>
  );
}

