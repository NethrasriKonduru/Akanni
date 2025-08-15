import React, { useRef, useState, useEffect } from "react";
import "./Testimonials.css";

const testimonials = [
  {
    name: "Alice Johnson",
    role: "CEO, TechVision",
    text: "Working with this team was a delight! They delivered beyond our expectations."
  },
  {
    name: "Mark Thompson",
    role: "Founder, Startify",
    text: "Our new website boosted our sales by 40%! Highly recommend their services."
  },
  {
    name: "Sophia Lee",
    role: "Product Manager, CloudWave",
    text: "Professional, creative, and always on time. A pleasure to work with."
  },
  {
    name: "David Kim",
    role: "CTO, BrightApps",
    text: "Their mobile app solution transformed how our customers engage with us."
  },
  {
    name: "Emma Brown",
    role: "Marketing Head, BrandHub",
    text: "Beautiful design and a smooth process from start to finish."
  },
];

export default function Testimonials() {
  const trackRef = useRef(null);
  const [canLeft, setCanLeft] = useState(false);
  const [canRight, setCanRight] = useState(true);

  const CARD_WIDTH = 300;
  const SCROLL_PIXELS = CARD_WIDTH * 1.5;

  const updateButtons = () => {
    const el = trackRef.current;
    if (!el) return;
    setCanLeft(el.scrollLeft > 0);
    setCanRight(el.scrollLeft + el.clientWidth < el.scrollWidth - 1);
  };

  const scrollByAmount = (amount) => {
    trackRef.current?.scrollBy({ left: amount, behavior: "smooth" });
  };

  useEffect(() => {
    const el = trackRef.current;
    if (!el) return;
    updateButtons();
    const onScroll = () => updateButtons();
    const onResize = () => updateButtons();
    el.addEventListener("scroll", onScroll);
    window.addEventListener("resize", onResize);
    return () => {
      el.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onResize);
    };
  }, []);

  return (
    <section className="testimonials-section" id="testimonials">
      <div className="testimonials-header">
        <h2>What Our Clients Say</h2>
        <div className="controls">
          <button
            className="arrow left"
            onClick={() => scrollByAmount(-SCROLL_PIXELS)}
            disabled={!canLeft}
            aria-label="Scroll testimonials left"
          >
            ‹
          </button>
          <button
            className="arrow right"
            onClick={() => scrollByAmount(SCROLL_PIXELS)}
            disabled={!canRight}
            aria-label="Scroll testimonials right"
          >
            ›
          </button>
        </div>
      </div>

      <div className="testimonials-track" ref={trackRef}>
        {testimonials.map((t, i) => (
          <div className="testimonial-card" key={i}>
            <p className="testimonial-text">“{t.text}”</p>
            <h4>{t.name}</h4>
            <span className="testimonial-role">{t.role}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
