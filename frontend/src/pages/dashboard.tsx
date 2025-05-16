import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { isLoggedIn } from "@/lib/auth";

export default function DashboardPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }

    const socket = new WebSocket("ws://localhost:8000/ws/feed");

    socket.onmessage = (event) => {
      const newMessage = event.data;
      setMessages((prev) => [...prev, newMessage]);
    };

    socket.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>HustleHub Feed</h1>
      <p>You are successfully logged in.</p>

      <ul style={{ marginTop: "2rem" }}>
        {messages.map((msg, index) => (
          <li key={index} style={{ paddingBottom: "0.5rem" }}>
            {msg}
          </li>
        ))}
      </ul>

      <button
        onClick={() => {
          localStorage.removeItem("access_token");
          router.push("/login");
        }}
        style={{
          marginTop: "2rem",
          padding: "0.5rem 1rem",
          backgroundColor: "#333",
          color: "white",
          border: "none",
          borderRadius: "4px",
        }}
      >
        Logout
      </button>
    </div>
  );
}
