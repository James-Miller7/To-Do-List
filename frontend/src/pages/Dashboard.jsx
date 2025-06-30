import { useState, useEffect } from "react";
import React from "react";
import api, { setAuthToken } from "../api/client";
import { useNavigate } from "react-router-dom";
import AddItem from "../components/Additem";
import "../styles/dashboard.css";


export default function Dashboard() {
  const [items, setItems] = useState([]);
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate("/login")
      return;
    }
    setAuthToken(token);
    api.get("/items/")
      .then(res => setItems(res.data))
      .catch(() => alert("Failed to fetch items"));
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  }

  const reverse_status = async (id) => {
    try {
      await api.patch(`/items/${id}/complete`);
      setItems((prev) =>
        prev.map((i) => (i.id === id ? { ...i, complete: !i.complete } : i))
      );
    } catch (err) {
      alert("Unable to change status of item")
    }
  }

  const handle_delete = async (id) => {
    try {
      await api.delete(`/items/${id}`);
      setItems((prev) =>
        prev.filter((i) => (i.id != id))
      );
    } catch (err) {
      alert("Unable to delete item from list")
    }
  }

  const handle_add = async (newItem) => {
    try {
      const res = await api.post("/items/", newItem);
      setItems((prev) => [...prev, res.data]);
    } catch (err) {
      alert("Failed to add item")
    }
  }

  return (
    <div className="dashboard-container">
      <button className="logout-btn" onClick={handleLogout}>Logout</button>
      <h2>Your To-Do List Items</h2>
      <AddItem onAdd={handle_add} />
      <ul className="todo-list">
        {items.map(item => (
          <li key={item.id}>
            <span>
              <button onClick={() => reverse_status(item.id)}>
                {item.complete ? '✅' : '❌'}
              </button>
              {item.name}{": "}{item.description}
            </span>
            <button onClick={() => handle_delete(item.id)}>
              Remove Item
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

