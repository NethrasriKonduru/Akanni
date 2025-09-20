// App.jsx
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
import JoinFormPage from "./components/JoinFormPage"; // new form page

const HomePage = () => {
  return (
    <>
      <Navbar />
      <Hero />
      <About />
      <JoinSection />
      <Services />
      <Testimonials />
      <Footer />
    </>
  );
};

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/join-form" element={<JoinFormPage />} />
      </Routes>
    </Router>
  );
};

export default App;
