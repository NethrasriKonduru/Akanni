import React from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Services from "./components/Services";
import Testimonials from "./components/Testimonials";
import Footer from "./components/Footer";
const App = () => {
  return (
    <>
      <Navbar />
      <Hero/>
     <Services/>
     <Testimonials/>
     <Footer/>
    </>
  );
};

export default App;
