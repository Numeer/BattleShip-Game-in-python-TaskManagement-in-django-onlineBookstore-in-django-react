import React, {useState} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import NavBar from "./Navbar";

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
                setSuccess('Your Token ');
                setRedirectToNavbar(true);
            } else {
                setError('Failed to get token');
            }
        } catch (error) {
            if (error.response && error.response.data) {
                const errorMessages = Object.values(error.response.data).flat();
                setError(errorMessages);
            } else {
                setError('Invalid Credentials');
            }
        }
    };

    return (
        <>
            {success && (
                <div>
                    {redirectToNavbar ? <NavBar/> : null}
                    <h3 className="text-success">{success}</h3>

                </div>
            )}
            <div className="container mx-6">
                <h2>Login</h2>
                {Array.isArray(error) ? (
                    <div className="text-danger">
                        {error.map((errorMsg, index) => (
                            <p key={index}>{errorMsg}</p>
                        ))}
                    </div>
                ) : null}

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
                    <button className="btn btn-primary">Register</button>
                </Link>
                </p>
            </div>
        </>

    );
};

export default Login;
