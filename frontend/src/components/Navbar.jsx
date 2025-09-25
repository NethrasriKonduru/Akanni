import React, { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import "./Navbar.css";
import logo from "./logo.jpg";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") setDarkMode(true);
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.classList.add("theme-dark");
      root.classList.remove("theme-light");
      localStorage.setItem("theme", "dark");
    } else {
      root.classList.add("theme-light");
      root.classList.remove("theme-dark");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  const toggleMode = () => {
    setDarkMode(!darkMode);
  };

  const navItems = [
    { to: "/signup", label: "SignUp" },
    { to: "/login", label: "Login" },
    { to: "/blog", label: "Blog" },
  ];

  return (
    <nav className={`navbar ${darkMode ? "dark" : "light"}`}>
      <div className="nav-container">
        <Link to="/" className="logo-container" aria-label="Go to home">
          <img src={logo} alt="Akanní logo" className="logo-img" />
          <span className="logo-text">Àkanní</span>
        </Link>

        <ul id="primary-navigation" className={`nav-links ${isOpen ? "active" : ""}`}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.to;
            return (
              <li key={item.to} className={isActive ? "active" : ""}>
                <Link className="nav-link" to={item.to} onClick={() => setIsOpen(false)}>
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>

        <div className="actions">
          <button
            className="mode-toggle"
            onClick={toggleMode}
            aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
            aria-pressed={darkMode}
            title={darkMode ? "Light mode" : "Dark mode"}
          >
            {darkMode ? "🌞" : "🌙"}
          </button>

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
      </div>
    </nav>
  );
}

export default Navbar;
