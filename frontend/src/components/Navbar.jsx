import React, { useState } from "react";
import "./Navbar.css";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="logo">MyCompany</div>

      <div className={`nav-links ${isOpen ? "active" : ""}`}>
        <a href="#home" onClick={() => setIsOpen(false)}>Home</a>
        <a href="#about" onClick={() => setIsOpen(false)}>About</a>
        <a href="#services" onClick={() => setIsOpen(false)}>Services</a>
        <a href="#testimonials" onClick={() => setIsOpen(false)}>Testimonials</a>
        <a href="#contact" onClick={() => setIsOpen(false)}>Contact</a>
      </div>

      <div
        className={`hamburger ${isOpen ? "open" : ""}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span></span>
        <span></span>
        <span></span>
      </div>
    </nav>
  );
};

export default Navbar;
