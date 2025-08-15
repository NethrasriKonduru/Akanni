import React from "react";
import "./Footer.css";
import {
  FaTwitter,
  FaFacebookF,
  FaInstagram,
  FaMapMarkerAlt,
  FaPhoneAlt,
  FaPaperPlane,
} from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="overlay"></div> {/* Transparent layer */}
      <div className="container">
        
        {/* First Column */}
        <div className="footer-col">
          <h1 className="footer-logo" style={{fontWeight: "bold" }}>Akkani</h1>
          <h4>One stop solution for all content needs</h4>
          <h3 style={{fontWeight: "bold" }}>Create, Elevate, Innovate</h3>
          <div className="social-icons">
            <a href="#"><FaTwitter /></a>
            <a href="#"><FaFacebookF /></a>
            <a href="#"><FaInstagram /></a>
          </div>
        </div>

        {/* Second Column */}
        <div className="footer-col">
          <h2>Quick Links</h2>
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Works</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </div>

        {/* Third Column */}
        <div className="footer-col">
          <h2>Have a Question?</h2>
          <div className="contact-item">
            <FaMapMarkerAlt /> Kothrud, Pune 411038
          </div>
          <div className="contact-item">
            <FaPhoneAlt /> +9004138118
          </div>
          <div className="contact-item">
            <FaPaperPlane /> team.akkani@gmail.com
          </div>
        </div>

      </div>

      <div className="footer-bottom">
        Copyright ©2025 All rights reserved
      </div>
    </footer>
  );
}
