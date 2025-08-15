import React, { useState } from "react";
import "./Services.css";

export default function Services() {
  const [selected, setSelected] = useState(null);

  const services = [
    {
      title: "AI Graphic Designing & Prompt Engineering",
      icon: "🎨",
      points: [
        "AI-powered graphic design",
        "Branding & visual identity creation",
        "Custom AI art & creative prompts",
        "Social media creatives & ad banners"
      ]
    },
    {
      title: "Web Designing & UI/UX Designing (Figma & Prototyping)",
      icon: "💻",
      points: [
        "Responsive website development",
        "UI/UX design for websites & mobile apps",
        "Interactive prototypes in Figma",
        "Landing page creation",
        "Portfolio & e-commerce websites"
      ]
    },
    {
      title: "Digital Marketing & Content Creation",
      icon: "📢",
      points: [
        "Social media management",
        "SEO & SEM campaigns",
        "Influencer collaborations",
        "Blog, script & copywriting",
        "Video editing & reels production"
      ]
    },
    {
      title: "Research, Analytics & Consultancy",
      icon: "📊",
      points: [
        "Market research & competitor analysis",
        "Data-driven strategy building",
        "Business growth consultation",
        "Trend forecasting"
      ]
    },
    {
      title: "Cybersecurity Solutions & Auditing",
      icon: "🛡️",
      points: [
        "Website & app vulnerability testing",
        "Data protection & encryption solutions",
        "Cyber risk assessment",
        "Security training & awareness programs"
      ]
    }
  ];

  return (
    <section className="services-section">
      <h2 className="services-title">Our Services</h2>

      <div className="services-wrapper">
        {services.map((svc, i) => (
          <div
            className="service-card"
            key={i}
            onMouseEnter={() => setSelected(svc)}
            onMouseLeave={() => setSelected(null)}
          >
            <div className="service-icon">{svc.icon}</div>
            <h3>{svc.title}</h3>
          </div>
        ))}
      </div>

      {selected && (
        <div
          className="service-overlay"
          onMouseEnter={() => setSelected(selected)}
          onMouseLeave={() => setSelected(null)}
        >
          <div
            className="service-details"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="close-btn"
              onClick={() => setSelected(null)}
            >
              &times;
            </button>
            <div className="service-icon">{selected.icon}</div>
            <h3>{selected.title}</h3>
            <ul>
              {selected.points.map((p, idx) => (
                <li key={idx}>{p}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </section>
  );
}
