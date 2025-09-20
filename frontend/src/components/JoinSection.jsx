// JoinSection.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import "./JoinSection.css";
import heroImg from "./images/hero-bg.jpg";

function JoinSection() {
  const navigate = useNavigate();

  const handleJoinClick = () => {
    navigate("/join-form");
  };

  return (
    <section className="join-section">
      <div className="join-left">
        <img src={heroImg} alt="Join Us" />
      </div>

      <div className="join-right">
        <h2>Be a Part of Akanni</h2>
        <p>
          Join our community today and explore amazing features.
          Discover, connect, and grow with us on this journey.
        </p>
        <button className="join-btn" onClick={handleJoinClick}>
          Join Now
        </button>
      </div>
    </section>
  );
}

export default JoinSection;
