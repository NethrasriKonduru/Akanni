import React, { useEffect, useState, useRef } from "react";
import "./Testimonials.css";

const Testimonials = () => {
  const [testimonials, setTestimonials] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const videoRef = useRef(null);

  const handleVideoClick = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused) {
      videoRef.current.play();
      setIsPaused(true);
    } else {
      videoRef.current.pause();
      setIsPaused(false);
    }
  };

  const handleVideoEnded = () => {
    setIsPaused(false);
  };

  useEffect(() => {
    const API_URL = "https://akanni-b3bh.onrender.com/api/v1/testimonials/";

    fetch(API_URL)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        const updated = data.map((item) => {
          const videoBase64Data =
            item.video && item.video.content && item.video.content_type
              ? `data:${item.video.content_type};base64,${item.video.content}`
              : null;

          const imageBase64Data =
            item.image && item.image.content && item.image.content_type
              ? `data:${item.image.content_type};base64,${item.image.content}`
              : null;

          return {
            ...item,
            videoSource: videoBase64Data,
            imageSource: imageBase64Data,
          };
        });
        setTestimonials(updated);
      })
      .catch((err) => {
        console.error("Error fetching testimonials. Check Network/CORS:", err);
      });
  }, []);

  useEffect(() => {
    if (testimonials.length === 0 || isPaused) return;
    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [testimonials, isPaused]);

  if (testimonials.length === 0) return <p>Loading testimonials...</p>;

  const { name, rating, content, videoSource, imageSource } = testimonials[activeIndex];

  return (
    <div className="testimonials-container">
      <h1>What Our Clients Say</h1>
      <div className="testimonial-card">
        <div className="testimonial-text-wrapper">
          <div className="testimonial-image">
            {imageSource ? (
              <img src={imageSource} alt={`${name}'s photo`} className="client-photo" />
            ) : (
              <div style={{ padding: "20px", color: "#888", textAlign: "center" }}>
                No image available for this testimonial.
              </div>
            )}
          </div>
          <div className="testimonial-text">
            <h2 className="client-name">{name}</h2>
            <div className="stars">{"⭐".repeat(rating || 5)}</div>
            <p>{content}</p>
          </div>
        </div>
        <div className="testimonial-video">
          {videoSource ? (
            <video
              ref={videoRef}
              key={videoSource}
              onClick={handleVideoClick}
              onEnded={handleVideoEnded}
              width="300"
              style={{ cursor: "pointer" }}
              controls
              src={videoSource}
            >
              Your browser does not support video playback.
            </video>
          ) : (
            <div style={{ padding: "20px", color: "#888", textAlign: "center" }}>
              No video available for this testimonial.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Testimonials;
