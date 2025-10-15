import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";
import logo from "./logo.jpg";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { to: "/signup", label: "SignUp" },
    { to: "/login", label: "Login" },
    {  label: "Blog" },
  ];

  return (
    <nav className="navbar">
      <div className="nav-container">
        {/* Logo */}
        <Link to="/" className="logo-container" aria-label="Go to home">
          <img src={logo} alt="Akanní logo" className="logo-img" />
          <span className="logo-text">Àkanní</span>
        </Link>

        {/* Navigation links */}
        <ul className={`nav-links ${isOpen ? "active" : ""}`}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.to;
            return (
              <li key={item.to} className={isActive ? "active" : ""}>
                <Link
                  className="nav-link"
                  to={item.to}
                  onClick={() => setIsOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>

        {/* Mobile menu button */}
        <button
          className="mobile-menu-icon"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle navigation"
          aria-controls="primary-navigation"
          aria-expanded={isOpen}
        >
          {isOpen ? "✖" : "☰"}
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
