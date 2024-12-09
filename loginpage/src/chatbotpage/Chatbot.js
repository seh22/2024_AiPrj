import React from "react";
import { useLocation } from "react-router-dom";

const Chatbot = () => {
  const location = useLocation();
  const userInfo = location.state;

  return (
    <div>
      <h1>Welcome to Chatbot!</h1>
      <p>Name: {userInfo?.name}</p>
      <p>Email: {userInfo?.email}</p>
    </div>
  );
};

export default Chatbot;
