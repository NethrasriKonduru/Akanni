import React from "react";
import "./testimonials.css";

const testimonialsData = [
  {
    name: "John Doe",
    image: "person1.jpg",
    rating: 5,
    text: "This product changed my life! The quality and service were beyond expectations."
  },
  {
    name: "Sarah Lee",
    image: "person2.jpg",
    rating: 4,
    text: "Excellent experience overall. I will definitely recommend it to my friends."
  },
  {
    name: "Michael Smith",
    image: "person3.jpg",
    rating: 5,
    text: "Great quality and very stylish. Fits perfectly with my expectations."
  }
];

const Testimonials = () => {
  return (
    <section className="testimonial-section">
      <div className="overlay"></div>
      <div className="testimonial-container">
        {testimonialsData.map((t, index) => (
          <div className="testimonial-card" key={index}>
            <img src={t.image} alt={t.name} />
            <h3>{t.name}</h3>
            <div className="stars">
              {"★".repeat(t.rating) + "☆".repeat(5 - t.rating)}
            </div>
            <p>{t.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Testimonials;

