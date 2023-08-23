import React, {useState} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import NavBar from "./Navbar";
import "../styles.css"
import InputField from "./inputField";

const Login = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const [errorMessage, setErrorMessage] = useState('');
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
        setErrorMessage('');
        setSuccess('');
        try {
            const response = await axios.post('http://127.0.0.1:8000/gettoken/', formData);


            if (response.data.token) {
                sessionStorage.setItem('authToken', response.data.token);
                sessionStorage.setItem('username', formData.username);
                sessionStorage.setItem('password', formData.password);
                setToken(response.data.token);
                setSuccess('Logged In Successfully');
                setRedirectToNavbar(true);

            } else {
                setErrorMessage('Failed to get token');
            }
        } catch (errorMessage) {
            if (!errorMessage?.response) {
                setErrorMessage('No Server Response');
            } else if (errorMessage.response?.status === 400) {
                setErrorMessage('Missing Username or Password');
            } else if (errorMessage.response?.status === 401) {
                setErrorMessage('Unauthorized');
            } else {
                setErrorMessage('Login Failed');
            }
        }
    };

    return (
        <>
            {redirectToNavbar ? <NavBar/> : null}
            <div className="container login-container my-5">
                <h3 className="text-success mt-3">{success}</h3>
                <h2>Login</h2>
                <p className="alert-danger" aria-live="assertive">{errorMessage}</p>
                <form onSubmit={handleSubmit}>
                    <InputField
                        label="Username"
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                    />
                    <InputField
                        label="Password"
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                    />
                    <button type="submit" className="btn btn-primary">
                        Login
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
