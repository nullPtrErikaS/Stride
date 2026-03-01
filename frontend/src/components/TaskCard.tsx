"use client";
import { useState, useEffect } from "react";
import API from "@/lib/api";

type Task = {
    id: string;
    content: string;
    timestamp: string;
};

export default function TaskCard({ task, refresh }: { task: Task, refresh: () => void }) {
    const [likes, setLikes] = useState(0);
    const [dislikes, setDislikes] = useState(0);

    useEffect(() => {
        API.get(`/reactions/task/${task.id}/summary`)
            .then(res => {
                setLikes(res.data.likes);
                setDislikes(res.data.dislikes);
            }).catch(() => { });
    }, [task.id]);

    const handleReaction = async (type: "like" | "dislike") => {
        try {
            await API.post(`/reactions/${task.id}/${type}`);
            // Refresh summary
            const res = await API.get(`/reactions/task/${task.id}/summary`);
            setLikes(res.data.likes);
            setDislikes(res.data.dislikes);
        } catch (e) {
            console.error(e);
        }
    };

    const handleDelete = async () => {
        try {
            await API.delete(`/tasks/${task.id}`);
            refresh();
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="p-5 border border-gray-200 rounded-lg shadow-sm bg-white mb-4 hover:shadow-md transition">
            <p className="text-lg text-gray-800 break-words">{task.content}</p>
            <div className="flex gap-4 mt-6 items-center">
                <button onClick={() => handleReaction("like")} className="text-green-700 font-medium bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded transition">
                    Like ({likes})
                </button>
                <button onClick={() => handleReaction("dislike")} className="text-red-700 font-medium bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded transition">
                    Dislike ({dislikes})
                </button>
                <button onClick={handleDelete} className="ml-auto text-gray-500 font-medium hover:text-red-600 text-sm py-1.5 px-3 rounded hover:bg-gray-100 transition">
                    Delete
                </button>
            </div>
        </div>
    );
}
