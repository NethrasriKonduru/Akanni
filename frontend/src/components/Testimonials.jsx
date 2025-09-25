import React, { useEffect, useState, useRef } from "react";
import "./Testimonials.css";

const dummyNames = ["Ananya Sharma", "John Doe", "Rahul Verma"];
const dummyTexts = [
  "Akanni transformed our digital presence completely. Their creativity and professionalism were outstanding.",
  "The team helped us launch faster than we expected. Truly a one-stop solution for startups!",
  "Great collaboration, excellent quality, and timely delivery. I’d definitely recommend Akanni."
];

const Testimonials = () => {
  const [testimonials, setTestimonials] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false); // auto-slide pause flag
  const videoRef = useRef(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/videos")
      .then((res) => res.json())
      .then((data) => {
        const updated = data.map((item, i) => ({
          ...item,
          name: dummyNames[i % dummyNames.length],
          rating: 5,
          content: dummyTexts[i % dummyTexts.length]
        }));
        setTestimonials(updated);
      })
      .catch((err) => console.error("Error fetching testimonials:", err));
  }, []);

  // Auto-slide
  useEffect(() => {
    if (testimonials.length === 0 || isPaused) return;

    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % testimonials.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [testimonials, isPaused]);

  if (testimonials.length === 0) return <p>Loading testimonials...</p>;

  const { name, rating, content, videoUrl } = testimonials[activeIndex];

  const handleVideoClick = () => {
    if (!videoRef.current) return;

    if (videoRef.current.paused) {
      videoRef.current.play();
      setIsPaused(true); // pause auto-slide while video plays
    } else {
      videoRef.current.pause();
      setIsPaused(false); // resume auto-slide if user stops video
    }
  };

  const handleVideoEnded = () => {
    setIsPaused(false); // resume auto-slide after video ends
  };

  return (
    <div className="testimonials-container">
      <h1>What Our Clients Say</h1>

      <div className="testimonial-card">
        <div className="testimonial-text">
          <h2 className="client-name">{name}</h2>
          <div className="stars">{"⭐".repeat(rating)}</div>
          <p>{content}</p>
        </div>

        <div className="testimonial-video">
          <video
            ref={videoRef}
            key={videoUrl}
            onClick={handleVideoClick}
            onEnded={handleVideoEnded}
            width="300"
            style={{ cursor: "pointer" }}
          >
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support video playback.
          </video>
        </div>
      </div>
    </div>
  );
};

export default Testimonials;

