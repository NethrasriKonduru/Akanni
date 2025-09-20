import React, { useState } from "react";
import "./JoinFormPage.css";

function JoinFormPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    contact: "",
    degree: "",
    customDegree: "",
    isStudying: "",
    course: "",
    experience: "",
    domains: [],
  });

  const services = ["AI Graphics", "Web & UI/UX", "Digital Marketing", "Analytics & Research", "Cybersecurity"];
  
  const degreeOptions = [
    "High School",
    "Diploma",
    "B.Sc",
    "B.Com",
    "B.A",
    "B.Tech",
    "M.Sc",
    "M.Com",
    "M.A",
    "MBA",
    "Other"
  ];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      let updatedDomains = [...formData.domains];
      if (checked) updatedDomains.push(value);
      else updatedDomains = updatedDomains.filter((d) => d !== value);
      setFormData({ ...formData, domains: updatedDomains });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Use customDegree if degree === 'Other'
    const finalDegree = formData.degree === "Other" ? formData.customDegree : formData.degree;
    console.log({ ...formData, degree: finalDegree });
    alert("Form submitted! Check console for details.");
  };

  return (
    <div className="form-page">
      <div className="form-card">
        <h2 className="form-title">Join Akanni</h2>
        <p className="form-subtitle">Become part of our amazing community</p>
        <form onSubmit={handleSubmit} className="join-form">

          <div className="form-row">
            <div className="form-group">
              <label>Name</label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </div>
          </div>

          <div className="form-group">
            <label>Contact Number</label>
            <input type="tel" name="contact" value={formData.contact} onChange={handleChange} required />
          </div>

          {/* Degree dropdown */}
          <div className="form-group">
            <label>Degree</label>
            <select name="degree" value={formData.degree} onChange={handleChange} required>
              <option value="">Select your degree</option>
              {degreeOptions.map((deg) => (
                <option key={deg} value={deg}>{deg}</option>
              ))}
            </select>
          </div>

          {/* Show custom input if Other is selected */}
          {formData.degree === "Other" && (
            <div className="form-group">
              <label>Enter your degree</label>
              <input type="text" name="customDegree" value={formData.customDegree} onChange={handleChange} required />
            </div>
          )}

          <div className="form-group">
            <label>Are you studying?</label>
            <div className="radio-group">
              <label>
                <input type="radio" name="isStudying" value="yes" checked={formData.isStudying === "yes"} onChange={handleChange} required /> Yes
              </label>
              <label>
                <input type="radio" name="isStudying" value="no" checked={formData.isStudying === "no"} onChange={handleChange} /> No
              </label>
            </div>
          </div>

          {formData.isStudying === "yes" && (
            <div className="form-group">
              <label>What are you studying?</label>
              <input type="text" name="course" value={formData.course} onChange={handleChange} required />
            </div>
          )}

          {formData.isStudying === "no" && (
            <div className="form-group">
              <label>Work Experience (years)</label>
              <input type="number" name="experience" value={formData.experience} onChange={handleChange} required />
            </div>
          )}

          <div className="form-group">
            <label>Interested Domains/Services</label>
            <div className="checkbox-group">
              {services.map((service) => (
                <label key={service}>
                  <input type="checkbox" name="domains" value={service} checked={formData.domains.includes(service)} onChange={handleChange} />
                  {service}
                </label>
              ))}
            </div>
          </div>

          <button type="submit" className="submit-btn">Join Now</button>
        </form>
      </div>
    </div>
  );
}

export default JoinFormPage;
