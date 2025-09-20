import React, { useState } from "react";
import "./LoginPage.css";

function LoginPage() {
  const [formData, setFormData] = useState({
    emailOrMobile: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

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
      // Add API call here
    }
  };

  return (
    <div className="login-page">
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
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && (
              <span className="error">{errors.password}</span>
            )}
          </div>

          <button type="submit" className="login-btn">
            Login
          </button>

          <div className="divider">OR</div>

          <button type="button" className="google-btn">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"
              alt="Google"
            />
            Continue with Google
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
