"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import API from "@/lib/api";
import TaskCard from "@/components/TaskCard";

type Task = {
    id: string;
    content: string;
    timestamp: string;
};

export default function Dashboard() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [newTask, setNewTask] = useState("");
    const router = useRouter();

    const fetchTasks = async () => {
        try {
            const res = await API.get("/tasks/");
            setTasks(res.data);
        } catch (err: any) {
            if (err.response?.status === 401) {
                localStorage.removeItem("token");
                router.push("/login");
            }
        }
    };

    useEffect(() => {
        fetchTasks();
    }, []);

    const handlePost = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTask.trim()) return;
        try {
            await API.post("/tasks/", { content: newTask });
            setNewTask("");
            fetchTasks();
        } catch (err) {
            console.error(err);
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        router.push("/");
    };

    return (
        <div className="min-h-screen bg-gray-50 pb-12">
            <header className="bg-white shadow">
                <div className="max-w-4xl mx-auto px-4 py-6 flex justify-between items-center">
                    <h1 className="text-3xl font-bold text-gray-900">Stride Dashboard</h1>
                    <button onClick={logout} className="text-red-600 font-medium hover:text-red-800 bg-red-50 px-4 py-2 rounded-lg hover:bg-red-100 transition">
                        Logout
                    </button>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 mt-8">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
                    <h2 className="text-xl font-semibold mb-4 text-gray-800">Share your current hustle</h2>
                    <form onSubmit={handlePost} className="flex gap-4 flex-col sm:flex-row">
                        <input
                            type="text"
                            value={newTask}
                            onChange={(e) => setNewTask(e.target.value)}
                            placeholder="What are you working on right now?"
                            className="flex-1 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                        />
                        <button type="submit" className="bg-blue-600 text-white font-medium p-3 rounded hover:bg-blue-700 transition sm:w-auto w-full">
                            Post Task
                        </button>
                    </form>
                </div>

                <div className="space-y-4">
                    <h2 className="text-xl font-semibold text-gray-800">Your Feed</h2>
                    {tasks.length === 0 ? (
                        <p className="text-gray-500">No tasks posted yet. Get to hustling!</p>
                    ) : (
                        tasks.map(task => (
                            <TaskCard key={task.id} task={task} refresh={fetchTasks} />
                        ))
                    )}
                </div>
            </main>
        </div>
    );
}
