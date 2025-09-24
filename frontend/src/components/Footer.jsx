import React from "react";
import "./Footer.css";
import { FaDribbble, FaInstagram, FaBehance, FaTwitter, FaLinkedin, FaGithub, FaWhatsapp } from "react-icons/fa";
import { FaRegEnvelope } from "react-icons/fa";
import { useState } from "react";
import { Link } from "react-router-dom";
const Footer = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubscribe = () => {
    if (!email) {
      setMessage("Please enter your email.");
      return;
    }

    // simple email regex validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setMessage("Please enter a valid email address.");
      return;
    }

    // 👉 here you can send email to backend API / Firebase / Mailchimp
    console.log("Subscribed with email:", email);

    setMessage("✅ Thank you for subscribing!");
    setEmail(""); // clear input
  };

  return (
    <footer className="footer">
      <div className="footer-container">

        {/* Left Section - Newsletter */}
        <div className="footer-left">
          <h2>Subscribe to stay in touch with the latest Services.</h2>
          <div className="newsletter">
            <input
              type="email"
              placeholder="Your email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <button onClick={handleSubscribe}>
              <FaRegEnvelope />
            </button>
          </div>
          { message && <p className="subscribe-message">{message}</p>}

          <p className="follow-text">FOLLOW US HERE:</p>
          <div className="social-icons">
            <a href="https://www.instagram.com/_.akanni.__/?igsh=MW11ZW96dWs5YTRmOQ%3D%3D#" target="_blank" rel="noopener noreferrer">
            <FaInstagram /></a>
            <FaTwitter />
            <a href="https://www.linkedin.com/company/akanni-team-ab0047342/" target="_blank" rel="noopener noreferrer">
            <FaLinkedin /></a>
            <FaGithub />
          </div>
        </div>

        {/* Middle Section - Links */}
        <div className="footer-middle">
           <h3>Quick Links</h3>
  <ul>
    <li><Link to="/">Home</Link></li>
    <li><Link to="/about">About Us</Link></li>
    <li><Link to="/services">Services</Link></li>
    <li><Link to="/testimonials">Testimonials</Link></li>
    <li><Link to="/contact">Contact Us</Link></li>
    <li><Link to="/blog">Blog</Link></li>
  </ul>
</div>

        {/* Right Section - Contact Info */}
        <div className="footer-right">
  <p className="label">DROP US A LINE</p>
  <p className="email">
    <a href="mailto:team.akanni@gmail.com">team.akanni@gmail.com</a>
  </p>

  <p className="label">CALL US</p>
  <p className="phone">
    <a
      href="https://wa.me/9004138118"
      target="_blank"
      rel="noopener noreferrer"
    >
      <FaWhatsapp className="whatsapp" /> +91 9004138118
    </a>
  </p>
</div>

      </div>
    </footer>
  );
};

export default Footer;
