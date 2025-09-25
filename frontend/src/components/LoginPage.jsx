import React, { useState } from "react";
import background from "./images/background.jpg"; // adjust path
import "./LoginPage.css";
import { FcGoogle } from "react-icons/fc";
import { FaLinkedin } from "react-icons/fa";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [formData, setFormData] = useState({
    emailOrMobile: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.emailOrMobile)
      newErrors.emailOrMobile = "Email or Mobile is required";
    if (!formData.password) newErrors.password = "Password is required";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      console.log("Login Data:", formData);
      alert("Login Successful!");
    }
  };

  return (
    <div
      className="login-page"
      style={{
        backgroundImage: `url(${background})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        width: "100vw",
        height: "100vh",
      }}
    >
      <div className="login-page-right">
        <div className="login-card">
          <h2 className="login-title">Login to Your Account</h2>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label>Email or Mobile</label>
              <input
                type="text"
                name="emailOrMobile"
                value={formData.emailOrMobile}
                onChange={handleChange}
              />
              {errors.emailOrMobile && (
                <span className="error">{errors.emailOrMobile}</span>
              )}
            </div>

            <div className="form-group">
              <label>Password</label>
            <div className="input-with-toggle">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={formData.password}
                onChange={handleChange}
              />
              <button
                type="button"
                className="toggle-visibility"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
              {errors.password && (
                <span className="error">{errors.password}</span>
              )}
            </div>

            <button type="submit" className="login-btn">
              Login
            </button>

            <div className="divider">OR</div>

            <button type="button" className="google-btn">
              <FcGoogle size={24} style={{ marginRight: "10px" }} />
              Continue with Google
            </button>

            <button type="button" className="linkedin-btn">
              <FaLinkedin size={24} style={{ marginRight: "10px" }} />
              Continue with LinkedIn
            </button>
          </form>

          <div className="auth-redirect">
            Don't have an account? {" "}
            <button type="button" className="link-button" onClick={() => navigate("/signup")}>Sign up</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
