import Login from "./auth/Login"
import Dashboard from "./pages/dashboard"
import Signup from "./auth/Signup";
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import React, { useEffect } from "react";
import { setAuthToken } from "./api/client";

function App() {
  const token = localStorage.getItem("token");
  if (token) {
    setAuthToken(token);
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/dashboard"
          element={token ? <Dashboard /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/"
          element={token ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App
