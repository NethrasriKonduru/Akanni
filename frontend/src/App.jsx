import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Services from "./components/Services";
import Testimonials from "./components/Testimonials";
import Footer from "./components/Footer";
import SignupPage from "./components/SignupPage";
import LoginPage from "./components/LoginPage";
import JoinSection from "./components/JoinSection";
import About from "./components/Aboutus";
import JoinFormPage from "./components/JoinFormPage";
import ContactPage from "./components/ContactPage"; // make sure this exists
import Home from "./components/Hero"

// Home page component
// HomePage.jsx
const HomePage = () => {
  return (
    <>
      <Navbar />
      <main>
        <section id="home"><Hero /></section>
        <section id="about"><About /></section>
        <section id="join"><JoinSection /></section>
        <section id="services"><Services /></section>
        <section id="testimonials"><Testimonials /></section>
      </main>

      {/* Contact page will have its own route */}
      <Footer />
    </>
  );
};


// Main App component with routing
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/join-form" element={<JoinFormPage />} />
        <Route path="/home" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/services" element={<Services />} />
        <Route path="/testimonials" element={<Testimonials />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/blog" element={<LoginPage />} />
      </Routes>
    </Router>
  );
};


export default App;
