import logo from './logo.svg';
import './App.css';
import Loginpage from './loginpage/Loginpage'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Chatbot from './chatbotpage/Chatbot';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Loginpage />} />
        <Route path='/chatbot' element={<Chatbot/>}/>
      </Routes>
    </Router>
  );
}
export default App;
