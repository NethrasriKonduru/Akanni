import React, { useRef, useState, useEffect } from "react";
import "./Services.css";

const services = [
  { title: "Web Development", desc: "Modern, responsive websites." },
  { title: "UI/UX Design", desc: "Clean, user-centric interfaces." },
  { title: "Branding", desc: "Logos, color systems, identity." },
  { title: "SEO & Analytics", desc: "Get found. Learn from data." },
  { title: "E-Commerce", desc: "Shops, carts, payments." },
  { title: "Mobile Apps", desc: "iOS & Android experiences." },
  { title: "Cloud & DevOps", desc: "Deploys, CI/CD, reliability." },
  { title: "Support & Maintenance", desc: "Keep things running smooth." },
];

export default function Services() {
  const trackRef = useRef(null);
  const [canLeft, setCanLeft] = useState(false);
  const [canRight, setCanRight] = useState(true);

  const CARD_WIDTH = 280; // card width + gap (approx)
  const SCROLL_PIXELS = CARD_WIDTH * 2; // scroll 2 cards per click

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
    <section className="services-section" id="services">
      <div className="services-header">
        <h2>Our Services</h2>
        <div className="controls">
          <button
            className="arrow left"
            onClick={() => scrollByAmount(-SCROLL_PIXELS)}
            disabled={!canLeft}
            aria-label="Scroll services left"
          >
            ‹
          </button>
          <button
            className="arrow right"
            onClick={() => scrollByAmount(SCROLL_PIXELS)}
            disabled={!canRight}
            aria-label="Scroll services right"
          >
            ›
          </button>
        </div>
      </div>

      <div className="services-track" ref={trackRef}>
        {services.map((s, i) => (
          <article className="service-card" key={i}>
            <div className="icon-circle">{i + 1}</div>
            <h3>{s.title}</h3>
            <p>{s.desc}</p>
            <button className="card-btn">Learn more</button>
          </article>
        ))}
      </div>
    </section>
  );
}
