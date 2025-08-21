import React, { useState } from "react";
import "./Services.css";
import { 
  FaPalette, 
  FaLaptopCode, 
  FaBullhorn, 
  FaChartLine, 
  FaShieldAlt 
} from "react-icons/fa";

export default function Services() {
  const [selected, setSelected] = useState(null);

  const services = [
    {
      title: "AI Graphic Designing & Prompt Engineering",
      icon: <FaPalette />,
      points: [
        "AI-powered graphic design",
        "Branding & visual identity creation",
        "Custom AI art & creative prompts",
        "Social media creatives & ad banners",
      ],
    },
    {
      title: "Web Designing & UI/UX Designing (Figma & Prototyping)",
      icon: <FaLaptopCode />,
      points: [
        "Responsive website development",
        "UI/UX design for websites & mobile apps",
        "Interactive prototypes in Figma",
        "Landing page creation",
        "Portfolio & e-commerce websites",
      ],
    },
    {
      title: "Digital Marketing & Content Creation",
      icon: <FaBullhorn />,
      points: [
        "Social media management",
        "SEO & SEM campaigns",
        "Influencer collaborations",
        "Blog, script & copywriting",
        "Video editing & reels production",
      ],
    },
    {
      title: "Research, Analytics & Consultancy",
      icon: <FaChartLine />,
      points: [
        "Market research & competitor analysis",
        "Data-driven strategy building",
        "Business growth consultation",
        "Trend forecasting",
      ],
    },
    {
      title: "Cybersecurity Solutions & Auditing",
      icon: <FaShieldAlt />,
      points: [
        "Website & app vulnerability testing",
        "Data protection & encryption solutions",
        "Cyber risk assessment",
        "Security training & awareness programs",
      ],
    },
  ];

  return (
    <section className="services-section">
      <h2 className="services-title">Our Services</h2>
      <div className="services-circle-container">
        {services.map((svc, index) => (
          <div
            key={index}
            className="service-circle"
            onClick={() => setSelected(index)}
          >
            <div className="circle-icon">{svc.icon}</div>
            <span className="circle-title">{svc.title}</span>
          </div>
        ))}
      </div>

      {selected !== null && (
        <div
          className="service-overlay"
          onClick={() => setSelected(null)}
        >
          <div
            className="service-details"
            onClick={(e) => e.stopPropagation()}
          >
            <button className="close-btn" onClick={() => setSelected(null)}>
              &times;
            </button>
            <div className="service-icon-large">{services[selected].icon}</div>
            <h3>{services[selected].title}</h3>
            <ul>
              {services[selected].points.map((p, idx) => (
                <li key={idx}>{p}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </section>
  );
}
