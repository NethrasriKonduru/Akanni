import React, { useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import "./Footer.css";
import {
  FaInstagram,
  FaTwitter,
  FaLinkedin,
  FaGithub,
  FaWhatsapp,
  FaMapMarkerAlt,
} from "react-icons/fa";
import { FaRegEnvelope } from "react-icons/fa";
import { HashLink as Link } from "react-router-hash-link";

const Footer = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubscribe = () => {
    if (!email) {
      setMessage("Please enter your email.");
      return;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setMessage("Please enter a valid email address.");
      return;
    }
    console.log("Subscribed with email:", email);
    setMessage("✅ Thank you for subscribing!");
    setEmail("");
  }

  return (
    <footer className="footer">
      <div className="footer-container">
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
          {message && <p className="subscribe-message">{message}</p>}

          <p className="follow-text">FOLLOW US HERE:</p>
          <div className="social-icons">
            <a
              href="https://www.instagram.com/_.akanni.__/?igsh=MW11ZW96dWs5YTRmOQ%3D%3D#"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaInstagram />
            </a>
            <a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer">
              <FaTwitter />
            </a>
            <a
              href="https://www.linkedin.com/company/akanni-team-ab0047342/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaLinkedin />
            </a>
            <a
              href="https://www.github.com/NethrasriKonduru/Akanni"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaGithub />
            </a>
          </div>
        </div>

        {/* Middle Section - Quick Links */}
        <div className="footer-middle">
          <h3>Quick Links</h3>
          <ul>
            <li>
              <Link smooth to="/#home">Home</Link>
            </li>
            <li>
              <Link smooth to="/#about">About Us</Link>
            </li>
            <li>
              <Link smooth to="/#services">Services</Link>
            </li>
            <li>
              <Link smooth to="/#testimonials">Testimonials</Link>
            </li>
            <li>
              <RouterLink to="/contact">Contact Us</RouterLink>
            </li>
            <li>
              <RouterLink to="/blog">Blog</RouterLink>
            </li>
          </ul>
        </div>

        {/* Right Section */}
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

          <p className="label">LOCATION</p>
          <div className="contact-item">
            <a
              href="https://www.google.com/maps/place/Kothrud,+Pune,+Maharashtra"
              target="_blank"
              rel="noopener noreferrer"
              style={{ textDecoration: "none", color: "blue" }}
            >
              <FaMapMarkerAlt className="contact-icon" /> Kothrud, Pune 411038
            </a>
          </div>
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="footer-bottom">
        <p>
          &copy; {new Date().getFullYear()} Akanni. All Rights Reserved. |{" "}
          <a
            href="https://github.com/NethrasriKonduru/Akanni"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub Repo
          </a>
        </p>
      </div>
    </footer>
  );
};

export default Footer;