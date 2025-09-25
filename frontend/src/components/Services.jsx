import React from "react";
import "./Services.css";

const services = [
  { title: "AI Graphic Designing & Prompt Engineering", description: "AI-powered graphic design, Branding, Custom AI art, Social media creatives" },
  { title: "Web Designing & UI/UX Designing (Figma & Prototyping)", description: "Responsive websites, UI/UX design, Figma prototypes, Landing & portfolio pages" },
  { title: "Digital Marketing & Content Creation", description: "Social media management, SEO campaigns, Influencer collaborations, Content creation" },
  { title: "Research, Analytics & Consultancy", description: "Market research, Data-driven strategy, Business growth consultation, Trend analysis" },
  { title: "Cybersecurity Solutions & Auditing", description: "Website & app testing, Data protection, Cyber risk assessment, Security training" },
];

export default function Services() {
  return (
    <section id="services" className="services-section">
      <h1 className="services-heading">Our Services</h1>
      <section className="services">
        {services.map((service, index) => (
          <div className="service-card" key={index}>
            <h3>{service.title}</h3>
            <p>{service.description}</p>
          </div>
        ))}
      </section>

    </section>
  );
}
