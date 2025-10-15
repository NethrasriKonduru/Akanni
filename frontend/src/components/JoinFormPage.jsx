import React, { useState } from "react";
import "./JoinFormPage.css";
import joinImg from "../assets/join-illustration.jpg"; // replace with your actual image

const JoinFormPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    contact: "",
    degree: "",
    studying: "",
    studyingDetails: "",
    experience: "",
    domains: [],
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === "checkbox") {
      setFormData((prev) => {
        const updatedDomains = checked
          ? [...prev.domains, value]
          : prev.domains.filter((d) => d !== value);
        return { ...prev, domains: updatedDomains };
      });
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
    alert("Form submitted!");
  };

  return (
    <div className="join-page">
      <div className="join-card">
        {/* Left Side - Form */}
        <div className="join-form-section">
          <h1 className="form-title">Join Akanni</h1>
          <p className="form-subtitle">Let’s start your journey with us!</p>

          <form className="join-form" onSubmit={handleSubmit}>
            {/* Name and Email */}
            <div className="form-row">
              <div className="form-group">
                <label>Name</label>
                <input
                  type="text"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                />
              </div>
            </div>

            {/* Contact Number */}
            <div className="form-group">
              <label>Contact Number</label>
              <input
                type="tel"
                name="contact"
                required
                value={formData.contact}
                onChange={handleChange}
              />
            </div>

            {/* Are you studying? */}
            <div className="form-group radio-group">
              <label>Are you studying?</label>
              <div>
                <label>
                  <input
                    type="radio"
                    name="studying"
                    value="Yes"
                    onChange={handleChange}
                  />{" "}
                  Yes
                </label>
                <label>
                  <input
                    type="radio"
                    name="studying"
                    value="No"
                    onChange={handleChange}
                  />{" "}
                  No
                </label>
              </div>
            </div>

            {/* Conditional Fields */}
            {formData.studying === "Yes" && (
              <div className="form-group">
                <label>What are you studying?</label>
                <select
                  name="studyingDetails"
                  required
                  value={formData.studyingDetails}
                  onChange={handleChange}
                >
                  <option value="">Select</option>
                  <option value="B.Tech">B.Tech</option>
                  <option value="M.Tech">M.Tech</option>
                  <option value="B.Sc">B.Sc</option>
                  <option value="BBA">BBA</option>
                  <option value="MBA">MBA</option>
                  <option value="Schooling">Schooling</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            )}

            {formData.studying === "No" && (
              <div className="form-group">
                <label>Experience (years)</label>
                <input
                  type="number"
                  name="experience"
                  placeholder="Enter your work experience"
                  value={formData.experience}
                  onChange={handleChange}
                />
              </div>
            )}

            {/* Interested Domains */}
            <div className="form-group checkbox-group">
              <label>Interested Domains/Services</label>
              {[
                "AI Graphics",
                "Web & UI/UX",
                "Digital Marketing",
                "Analytics & Research",
                "Cybersecurity",
              ].map((domain) => (
                <label key={domain}>
                  <input
                    type="checkbox"
                    name="domains"
                    value={domain}
                    onChange={handleChange}
                  />{" "}
                  {domain}
                </label>
              ))}
            </div>

            <button className="submit-btn" type="submit">
              Join Now
            </button>
          </form>
        </div>

        {/* Right Side - Image */}
        <div className="join-image-section">
          <img src={joinImg} alt="Join Akanni" />
        </div>
      </div>
    </div>
  );
};

export default JoinFormPage;
