import React from "react";
import "./Services.css";

const services = [
  { title: "AI Graphic Designing & Prompt Engineering"},
  { title: "Web Designing & UI/UX Designing (Figma & Prototyping)"},
  { title: "Digital Marketing & Content Creation"},
  { title: "Research, Analytics & Consultancy"},
  { title: "Cybersecurity Solutions & Auditing"},
];

export default function Services() {
  return (
    <section id="services" className="services-section">
      <h1 className="services-heading">Our Services</h1>
      <section className="services">
        {services.map((service, index) => (
          <div className="service-card" key={index}>
            <h3>{service.title}</h3>
          </div>
        ))}
      </section>

    </section>
  );
}
