import React, { useRef } from "react";
import "./Testimonials.css";

// Example images stored in public folder or imported
import client1 from "./images/client1.jpg";
import client2 from "./images/client2.jpg";
import client3 from "./images/client3.jpg";
import client4 from "./images/client4.jpg";

export default function Testimonials() {
  const wrapperRef = useRef(null);

  const testimonials = [
    {
      name: "Sravani Irigela",
      role: "Entrepreneur",
      feedback:
        "Amazing service! The AI graphics and web designs exceeded my expectations.",
      image: client1,
    },
    {
      name: "John Doe",
      role: "Marketing Manager",
      feedback:
        "Their digital marketing strategies boosted our engagement significantly.",
      image: client2,
    },
    {
      name: "Jane Smith",
      role: "Startup Founder",
      feedback:
        "Consultancy and analytics helped us make data-driven decisions effortlessly.",
      image: client3,
    },
    {
      name: "Alex Johnson",
      role: "Cybersecurity Head",
      feedback:
        "Professional security auditing with detailed reports and actionable insights.",
      image: client4,
    },
  ];

  const scroll = (direction) => {
    if (wrapperRef.current) {
      wrapperRef.current.scrollBy({
        left: direction === "left" ? -300 : 300,
        behavior: "smooth",
      });
    }
  };

  return (
    <section className="testimonials-section">
      <h2 className="testimonials-title">What Our Clients Say</h2>

      <div className="testimonials-container">
        <button className="scroll-btn left" onClick={() => scroll("left")}>
          &#8592;
        </button>

        <div className="testimonials-wrapper" ref={wrapperRef}>
          {testimonials.map((t, i) => (
            <div className="testimonial-card" key={i}>
              <img src={t.image} alt={t.name} className="testimonial-img" />
              <p className="feedback">"{t.feedback}"</p>
              <h4 className="name">{t.name}</h4>
              <span className="role">{t.role}</span>
            </div>
          ))}
        </div>

        <button className="scroll-btn right" onClick={() => scroll("right")}>
          &#8594;
        </button>
      </div>
    </section>
  );
}
