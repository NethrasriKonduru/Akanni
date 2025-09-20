import React from "react";
import "./Footer.css";
import {
  FaTwitter,
  FaFacebookF,
  FaInstagram,
<<<<<<< HEAD
  FaMapMarkerAlt,
  FaPhoneAlt,
  FaPaperPlane,
} from "react-icons/fa";
=======
  FaPaperPlane,
} from "react-icons/fa6";
import { FaPhoneAlt,FaMapMarkerAlt } from "react-icons/fa";
>>>>>>> cbb0c7dceb3dbb60a6331e0472d3dfe00850e9ea

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">

        
        <div className="footer-col">
          <h1 className="footer-logo" style={{ fontWeight: "bold" }}>Akanni</h1>
          <h4>One stop solution for all content needs</h4>
          <h3 style={{ fontWeight: "bold" }}>Create, Elevate, Innovate</h3>
          <div className="social-icons">
            <a href="#" className="social-twitter"><FaTwitter /></a>
            <a href="#" className="social-facebook"><FaFacebookF /></a>
            <a href="#" className="social-instagram"><FaInstagram /></a>
          </div>
        </div>

        
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

        
        <div className="footer-col">
          <h2>Have a Question?</h2>
          <div className="contact-item">
            <FaMapMarkerAlt className="contact-icon" /> Kothrud, Pune 411038
          </div>
          <div className="contact-item">
            <FaPhoneAlt className="contact-icon" /> +9004138118
          </div>
          <div className="contact-item">
            <FaPaperPlane className="contact-icon" /> team.akkani@gmail.com
          </div>
        </div>

      </div>

      <div className="footer-bottom">
        Copyright ©2025 All rights reserved
      </div>
    </footer>
  );
}
