//import React from 'react';
import { FaUser, FaEnvelope, FaLock } from 'react-icons/fa';
import './SignUpForm.css';

const SignUpForm = () => {
  return (
    <div className="container">
      <div className="form-wrapper">
        <h1 className="title">Sign Up</h1>
        <form className="form">
          <div className="input-group">
            <FaUser className="icon" />
            <input type="text" placeholder="Name" required />
          </div>
          <div className="input-group">
            <FaEnvelope className="icon" />
            <input type="email" placeholder="Email ID" required />
          </div>
          <div className="input-group">
            <FaLock className="icon" />
            <input type="password" placeholder="Password" required />
          </div>
          <div className="button-group">
            <button type="submit" className="btn btn-signup">
              Sign Up
            </button>
            <button type="button" className="btn btn-login">
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignUpForm;
