import React, { useRef } from "react";
import "./Testimonials.css";

const Testimonials = () => {
  const scrollRef = useRef(null);

  const scroll = (direction) => {
    if (direction === "left") {
      scrollRef.current.scrollBy({ left: -300, behavior: "smooth" });
    } else {
      scrollRef.current.scrollBy({ left: 300, behavior: "smooth" });
    }
  };

  return (
    <section className="testimonials-section">
      <h2 className="section-title">What Our Clients Say</h2>
      <div className="scroll-buttons">
        <button onClick={() => scroll("left")}>&lt;</button>
        <button onClick={() => scroll("right")}>&gt;</button>
      </div>
      <div className="testimonials-container" ref={scrollRef}>
        {[...Array(5)].map((_, index) => (
          <div className="testimonial-card" key={index}>
            <p>
              "This company is amazing! They really care about their customers."
            </p>
            <h4>- Client {index + 1}</h4>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Testimonials;
