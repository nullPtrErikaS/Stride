"use client";
import AuthForm from "@/components/AuthForm";

export default function LoginPage() {
    return (
        <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 px-6 lg:px-8">
            <AuthForm type="login" />
        </div>
    );
}
