import React from "react";
import "./Testimonials.css";
import shoeImage from "../assets/shoe.jpg"; // Background if needed

// Text Testimonials
const textTestimonials = [
  {
    name: "John Doe",
    role: "Entrepreneur",
    image: "https://via.placeholder.com/80",
    text: "I highly recommend them! The work was excellent.",
    rating: 5
  },
  {
    name: "Sarah Lee",
    role: "CEO, Company",
    image: "https://via.placeholder.com/80",
    text: "Great service and quick delivery. Really impressed!",
    rating: 4
  },
  {
    name: "Tom Hanks",
    role: "Actor",
    image: "https://via.placeholder.com/80",
    text: "They made the process so easy and stress-free.",
    rating: 5
  }
];

// Video Testimonials
const videoTestimonials = [
  {
    name: "Alice Johnson",
    role: "Designer",
    video: "/videos/review1.mp4"
  },
  {
    name: "Mark Smith",
    role: "Developer",
    video: "/videos/review2.mp4"
  }
];

const Testimonials = () => {
  return (
    <section className="testimonials-section">
      <h2 className="testimonials-title">What Our Clients Say</h2>
      <div className="testimonials-carousel">
        {textTestimonials.map((t, index) => (
          <div className="testimonial-card" key={`text-${index}`}>
            <img src={t.image} alt={t.name} className="testimonial-avatar" />
            <h4>{t.name}</h4>
            <p className="role">{t.role}</p>
            <p className="text">{t.text}</p>
            <p className="stars">{"⭐".repeat(t.rating)}</p>
          </div>
        ))}

        {videoTestimonials.map((v, index) => (
          <div className="testimonial-card video-card" key={`video-${index}`}>
            <video
              src={v.video}
              autoPlay
              muted
              loop
              playsInline
              className="testimonial-video"
            />
            <h4>{v.name}</h4>
            <p className="role">{v.role}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Testimonials;


