import React, { useState } from 'react';
import './Loginpage.css';
import CreateIcon from '@mui/icons-material/Create';
import { useNavigate } from 'react-router-dom';

const SignInSignUp = () => {
  const [isActive, setIsActive] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [userInfo, setUserInfo] = useState(null);
  const navigate = useNavigate();

  const handleSignUpClick = () => {
    if (!isActive) {
      setIsActive(true);
    }
  };

  const handleClose = (e) => {
    e.stopPropagation();
    setIsActive(false);
    setFormData({ name: '', email: '', password: '' });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSignUp = (e) => {
    e.stopPropagation();
    const { name, email, password } = formData;
    if (name === '' || email === '' || password === '') {
      alert('All fields are required!');
      return;
    }
    console.log('Sign Up Successful:', formData);
    setUserInfo({ name, email }); // 사용자 정보를 저장
    setIsActive(false);
    setFormData({ name: '', email: '', password: '' });
    alert('Sign up successful! Please sign in.');
  };

  const handleSignIn = () => {
    if (!userInfo) {
      alert('Please sign up first.');
      return;
    }
    console.log('Navigating to Chatbot with userInfo:', userInfo);
    navigate('/chatbot', { state: userInfo }); // navigate를 사용하여 정보 전달
  };

  return (
    <div className="login-container">
      
      <header>
        <h1>정신 건강 상담 챗봇</h1>
      </header>
      
      <div className="box">
        
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button onClick={handleSignIn}>Sign in</button>

        <div
          className={`sign-up-box ${isActive ? 'active' : ''}`}
          onClick={handleSignUpClick}
        >
          {!isActive ? (
            <CreateIcon className="material-icons" />
          ) : (
            <>
              <span onClick={handleClose}>X</span>
              <input
                type="text"
                name="name"
                placeholder="Name"
                value={formData.name}
                onChange={handleInputChange}
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleInputChange}
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
              />
              <button onClick={handleSignUp}>Sign up</button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SignInSignUp;
