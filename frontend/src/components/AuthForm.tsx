"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AuthForm({ type }: { type: "login" | "register" }) {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const endpoint = type === "login" ? "login" : "register";
      const body =
        type === "login"
          ? new URLSearchParams({ email, password })
          : JSON.stringify({ email, password, username });

      const res = await fetch(`http://localhost:8000/auth/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type":
            type === "login"
              ? "application/x-www-form-urlencoded"
              : "application/json",
        },
        body,
      });

      const data = await res.json();
      if (!res.ok) {
        let errorMessage = "Authentication Failed";
        if (data.detail) {
          errorMessage =
            typeof data.detail === "string"
              ? data.detail
              : Array.isArray(data.detail)
                ? data.detail[0].msg
                : JSON.stringify(data.detail);
        }
        throw new Error(errorMessage);
      }

      if (type === "login") {
        localStorage.setItem("token", data.access_token);
        router.push("/dashboard");
      } else {
        router.push("/login");
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-md mt-10 border border-gray-200">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-900">
        {type === "login" ? "Login" : "Register"}
      </h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {type === "register" && (
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white hover:bg-gray-50"
            required
          />
        )}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white hover:bg-gray-50"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white hover:bg-gray-50"
          required
        />
        <button
          type="submit"
          className="bg-blue-600 text-white font-medium p-3 rounded hover:bg-blue-700 transition"
        >
          {type === "login" ? "Login" : "Register"}
        </button>
      </form>
      {error && <p className="text-red-500 mt-4 text-center">{error}</p>}
      <div className="mt-4 text-center text-gray-600">
        {type === "login" ? (
          <p>
            Don't have an account?{" "}
            <a href="/register" className="text-blue-600 hover:underline">
              Register
            </a>
          </p>
        ) : (
          <p>
            Already have an account?{" "}
            <a href="/login" className="text-blue-600 hover:underline">
              Login
            </a>
          </p>
        )}
      </div>
    </div>
  );
}
