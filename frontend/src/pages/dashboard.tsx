import { useEffect } from "react";
import { useRouter } from "next/router";
import { isLoggedIn } from "@/lib/auth";

export default function DashboardPage() {
  const router = useRouter();

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
    }
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Welcome to HustleHub ✅</h1>
      <p>You are successfully logged in.</p>
      <button
        onClick={() => {
          localStorage.removeItem("access_token");
          router.push("/login");
        }}
        style={{
          marginTop: "1rem",
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
