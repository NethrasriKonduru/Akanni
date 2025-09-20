import React from "react";
import "./Hero.css";
import heroVideo from "./images/heroVideo.mp4"; // <-- put video inside src/components/images/

export default function Hero() {
  return (
    <section className="hero">
      {/* Background video */}
      <video autoPlay loop muted playsInline className="hero-video">
        <source src={heroVideo} type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* Overlay content */}
      <div className="hero-container">
        <div className="hero-text">
          <h1>Àkanní</h1>
          <p><strong>Powering Your Digital World with Cloud-Driven Excellence</strong></p>

        </div>
      </div>
    </section>
  );
}
