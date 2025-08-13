import React from "react";
import "./HeroSection.css";

const HeroSection = () => {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1>Welcome to Akaani</h1>
        <p>
          We craft innovative solutions to transform your business ideas into
          reality. Your vision, our expertise.
        </p>
        <div className="hero-buttons">
          <button className="btn primary">Get Started</button>
          <button className="btn secondary">Learn More</button>
        </div>
      </div>
      <div className="hero-image">
        <img
          src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f"
          alt="Business teamwork"
        />
      </div>
    </section>
  );
};

export default HeroSection;
