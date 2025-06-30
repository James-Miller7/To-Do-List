import { useState } from "react";
import api, { setAuthToken } from "../api/client";
import { useNavigate } from "react-router-dom";
import React from 'react';
import "../styles/signup.css";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const form = new FormData()
      form.append("username", username);
      form.append("password", password);
      await api.post("/signup/", form);

      const res = await api.post("/login/", form);
      const { access_token } = res.data
      localStorage.setItem("token", access_token)
      setAuthToken(access_token)
      navigate('/dashboard')
    } catch (err) {
      if (err.response) {
        const status = err.response.status;
        if (status === 400) {
          alert("Username is taken");
        } else {
          alert("Signup failed");
        }
      } else {
        alert("Something went wrong");
      }
    }
  }

  const toLogin = async (e) => {
    navigate("/login/")
  }

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSignup}>
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
        <button type="submit">Sign Up</button>
        <button type="button" onClick={toLogin} className="link-button">
          Go to Login
        </button>
      </form>
    </div>
  )

}