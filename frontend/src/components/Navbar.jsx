import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ import navigate
import "./Navbar.css";
import logo from "./logo.jpg";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isBig, setIsBig] = useState(false);
  const navigate = useNavigate(); // ✅ initialize navigate

  const handleLogoClick = () => {
    setIsBig(!isBig); // toggle logo size
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        {/* Logo */}
        <div className="logo-container">
          <img
            src={logo}
            alt="Logo"
            className={`logo-img ${isBig ? "big" : ""}`}
            onClick={handleLogoClick}
          />
          <h1 className="logo-text">Àkanní</h1>
        </div>

        {/* Navigation Links */}
        <ul className={`nav-links ${isOpen ? "active" : ""}`}>
          <li onClick={() => navigate("/signup")}>Signup</li>  {/* ✅ navigate */}
          <li onClick={() => navigate("/login")}>Login</li>    {/* ✅ navigate */}
          <li onClick={() => navigate("/blog")}>Blog</li>      {/* optional */}
        </ul>

        {/* Mobile Menu Icon */}
        <div
          className="mobile-menu-icon"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? "✖" : "☰"}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
