"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  const apiUrl = "http://localhost:5000";

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${apiUrl}/tasks`);
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error("Błąd przy pobieraniu tasków:", error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) return;

    const newTask = { title };

    try {
      const response = await fetch(`${apiUrl}/task`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newTask),
      });

      if (response.ok) {
        setTitle("");
        fetchTasks();
      } else {
        console.error("Błąd przy dodawaniu taska");
      }
    } catch (error) {
      console.error("Błąd:", error);
    }
  };

  return (
    <main style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h1>Todo App</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Wpisz nowe zadanie..." style={{ padding: "10px", width: "70%", marginRight: "10px" }} />
        <button type="submit" style={{ padding: "10px" }}>
          Dodaj
        </button>
      </form>

      <ul>
        {tasks.map((task, index) => (
          <li key={index} style={{ marginBottom: "10px" }}>
            {task.title}
          </li>
        ))}
      </ul>
    </main>
  );
}
