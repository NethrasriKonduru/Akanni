import React, { useState } from "react";
import "./ContactPage.css";
import contactImg from "./contact.png";  // 👈 Correct path

const ContactPage = () => {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Message sent successfully!");
    setFormData({ name: "", email: "", message: "" });
  };

  return (
    <div className="contact-container">
      <div className="contact-card">
        {/* Left Side */}
        <div className="contact-form">
          <h2>Contact Us</h2>
          <form onSubmit={handleSubmit}>
            <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
            <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
            <textarea name="message" placeholder="Message" value={formData.message} onChange={handleChange} required />
            <button type="submit">Send Message</button>
          </form>
        </div>

        {/* Right Side */}
        <div className="contact-illustration">
          <img src={contactImg} alt="Contact Illustration" />
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
