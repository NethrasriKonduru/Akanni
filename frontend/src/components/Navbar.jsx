import React, { useState } from "react";
import "./Navbar.css";
import logo from "./logo.jpg";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isBig, setIsBig] = useState(false);

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
            className={`logo-img ${isBig ? "big" : ""}`}  // ✅ correct syntax
            onClick={handleLogoClick}
          />
          <h1 className="logo-text">Àkanní</h1>
        </div>

        {/* Navigation Links */}
        <ul className={`nav-links ${isOpen ? "active" : ""}`}>
          <li>Departments</li>
          <li>Projects</li>
          <li>Blog</li>
          <li>Causes</li>
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
