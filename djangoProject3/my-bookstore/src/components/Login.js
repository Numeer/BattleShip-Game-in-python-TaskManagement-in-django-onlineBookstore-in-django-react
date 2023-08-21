import React, {useRef, useState, useEffect} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import NavBar from "./Navbar";
import "../styles.css"

const Login = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [token, setToken] = useState('');
    const [redirectToNavbar, setRedirectToNavbar] = useState(false);
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const response = await axios.post('http://127.0.0.1:8000/gettoken/', formData);

            if (response.data.token) {
                sessionStorage.setItem('authToken', response.data.token);
                sessionStorage.setItem('username', formData.username);
                setToken(response.data.token);
                setSuccess('Logged In Successfully');
                setRedirectToNavbar(true);
            } else {
                setError('Failed to get token');
            }
        } catch (error) {
            if (!error?.response) {
                setError('No Server Response');
            } else if (error.response?.status === 400) {
                setError('Missing Username or Password');
            } else if (error.response?.status === 401) {
                setError('Unauthorized');
            } else {
                setError('Login Failed');
            }
        }
    };

    return (
        <>
            {redirectToNavbar ? <NavBar/> : null}
            <div className="container login-container my-5">
                <h3 className="text-success mt-3">{success}</h3>
                <h2>Login</h2>
                <p className="alert-danger" aria-live="assertive">{error}</p>

                {token && (
                    <div className="alert alert-info" role="alert">
                        Token: {token}
                    </div>
                )}
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            className="form-control"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Get Token
                    </button>
                </form>
                <p className="mt-3">
                    Don't have an account? <Link to="/register">
                    <button className="btn btn-primary btn-lg">Register</button>
                </Link>
                </p>
            </div>
        </>

    );
};

export default Login;
