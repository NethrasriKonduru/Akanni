import React, { useRef } from "react";
import "./Services.css";

const Services = () => {
  const scrollRef = useRef(null);

  const scroll = (direction) => {
    if (direction === "left") {
      scrollRef.current.scrollBy({ left: -300, behavior: "smooth" });
    } else {
      scrollRef.current.scrollBy({ left: 300, behavior: "smooth" });
    }
  };

  const servicesData = [
    { title: "Web Development", description: "Build responsive and modern websites.", img: "https://via.placeholder.com/200" },
    { title: "App Development", description: "Mobile apps for Android and iOS.", img: "https://via.placeholder.com/200" },
    { title: "UI/UX Design", description: "Beautiful and intuitive designs.", img: "https://via.placeholder.com/200" },
    { title: "SEO Optimization", description: "Improve your search rankings.", img: "https://via.placeholder.com/200" },
    { title: "Cloud Services", description: "Secure and scalable cloud solutions.", img: "https://via.placeholder.com/200" },
  ];

  return (
    <div className="services-section">
      <h2 className="services-heading">Our Services</h2>
      <div className="services-wrapper">
        <button className="scroll-btn left" onClick={() => scroll("left")}>&lt;</button>
        <div className="services-container" ref={scrollRef}>
          {servicesData.map((service, index) => (
            <div className="service-card" key={index}>
              <img src={service.img} alt={service.title} />
              <h3>{service.title}</h3>
              <p>{service.description}</p>
            </div>
          ))}
        </div>
        <button className="scroll-btn right" onClick={() => scroll("right")}>&gt;</button>
      </div>
    </div>
  );
};

export default Services;
