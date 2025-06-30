import { useState } from "react";
import api, { setAuthToken } from "../api/client";
import { useNavigate } from "react-router-dom";
import React from 'react';
import "../styles/login.css";



export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const form = new FormData();
      form.append("username", username);
      form.append("password", password);
      const res = await api.post("/login/", form)

      const { access_token } = res.data;

      localStorage.setItem('token', access_token);

      setAuthToken(access_token);
      navigate('/dashboard');
    } catch (err) {
      if (err.response) {
        const status = err.response.status
        if (status === 400) {
          alert("Invalid credentials");
        } else {
          alert("Login Failed");
        }
      } else {
        alert("Something went wrong");
      }
    }
  }

  const toSignup = async (e) => {
    navigate("/signup/")
  }
  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          type="password"
        />
        <button type="submit">Login</button>
        <button type="button" onClick={toSignup} className="link-button">
          Go to Signup
        </button>
      </form>
    </div>
  );

}
