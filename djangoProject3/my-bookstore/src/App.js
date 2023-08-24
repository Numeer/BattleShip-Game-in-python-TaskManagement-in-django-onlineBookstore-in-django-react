import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import NavBar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Registration';
import UserList from './components/Users';
import BookDetail from "./components/BookDetail";
import { CartProvider } from "./context/CartContext";
import Store from "./components/Store";
import Cancel from "./Cancel";
import Success from "./Success";

class App extends Component {
  constructor() {
    super();
    this.state = {
      authToken: sessionStorage.getItem('authToken'),
    };
  }

  render() {
    const { authToken } = this.state;

    return (
      <Router>
        <AppContent authToken={authToken} />
      </Router>
    );
  }
}

function AppContent({ authToken }) {
  const location = useLocation();

  const isLoginPage = location.pathname === '/login';
  const isRegisterPage = location.pathname === '/register';

  return (
    <div>
      <CartProvider>
        {(!isLoginPage && !isRegisterPage) && <NavBar />}
        <Routes>
          <Route path="/books" element={<Store />} />
          <Route path="/books/:bookId" element={<BookDetail />} />
          <Route path="cancel" element={<Cancel />} />
          <Route path="success" element={<Success />} />
          <Route path="/login" element={authToken ? <Navigate to="/books" /> : <Login />} />
          <Route path="/user" element={<UserList />} />
          <Route path="/order/:orderId" element={<UserList />} />
          <Route path="/register" element={authToken ? <Navigate to="/books" /> : <Register />} />
          <Route path="/" element={authToken ? <Navigate to="/books" /> : <Navigate to="/login" />} />
        </Routes>
      </CartProvider>
    </div>
  );
}


export default App;
