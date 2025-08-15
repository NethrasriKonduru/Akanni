import React from "react";
import "./Footer.css";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-brand">
          <h2>MyCompany</h2>
          <p>Building dreams, one pixel at a time.</p>
        </div>

        <div className="footer-links">
          <a href="#services">Services</a>
          <a href="#testimonials">Testimonials</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
        </div>

        <div className="footer-social">
          <a href="https://facebook.com" target="_blank" rel="noreferrer">
            <i className="fab fa-facebook-f"></i>
          </a>
          <a href="https://twitter.com" target="_blank" rel="noreferrer">
            <i className="fab fa-twitter"></i>
          </a>
          <a href="https://instagram.com" target="_blank" rel="noreferrer">
            <i className="fab fa-instagram"></i>
          </a>
          <a href="https://linkedin.com" target="_blank" rel="noreferrer">
            <i className="fab fa-linkedin-in"></i>
          </a>
        </div>
      </div>

      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} MyCompany. All Rights Reserved.</p>
      </div>
    </footer>
  );
}
