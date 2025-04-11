//import React from 'react';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import './SignInForm.css';

const SignInForm = () => {
  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-logo">
          <h1>MindFeed</h1>
        </div>
        <form className="login-form">
          <div className="login-input-group">
            <FaEnvelope className="login-icon" />
            <input type="text" placeholder="Username or Email" required />
          </div>
          <div className="login-input-group">
            <FaLock className="login-icon" />
            <input type="password" placeholder="Password" required />
          </div>
          <button type="submit" className="login-btn">Login</button>
        </form>
        <div className="login-footer">
          <span>Don`t have an account? <Link to="/register" className="register-link">Register</Link></span>
        </div>
      </div>
    </div>
  );
};

export default SignInForm;
