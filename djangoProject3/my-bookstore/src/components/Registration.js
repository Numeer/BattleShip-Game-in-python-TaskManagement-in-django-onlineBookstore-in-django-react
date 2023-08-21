import React, {useState} from 'react';
import axios from 'axios';
import {Link} from "react-router-dom";
import NavBar from "./Navbar";

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        password2: '',
        email: '',
        first_name: '',
        last_name: '',
    });

    const [error, setErrors] = useState({});
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
        setErrors('');
        setSuccess('');

        try {
            const response = await axios.post('http://localhost:8000/register/', formData);
            console.log('Registration successful', response.data);
            sessionStorage.setItem('authToken', response.data.token);
            sessionStorage.setItem('username', formData.username);
            setToken(response.data.token);
            setSuccess('Registration successful');
            setRedirectToNavbar(true);

        } catch (error) {
            if (error.response) {
                const errorData = error.response.data;

                if (errorData.errors) {
                    setErrors(errorData.errors);
                } else if (errorData.message) {
                    setErrors({ global: errorData.message });
                }
            } else {
                setErrors({ global: 'No Server Response' });
            }
        }
    };

    return (
        <>
            {redirectToNavbar ? <NavBar/> : null}
            <div className="container login-container my-3">
                {success && (
                <div>
                    <h3 className="text-success">{success}</h3>
                </div>
            )}
                {Object.keys(error).length > 0 && (
                    <div className="alert alert-danger" role="alert">
                        {Object.keys(error).map((field, index) => (
                            <p key={index}>{error[field]}</p>
                        ))}
                </div>
            )}
                <h2>Register</h2>
                {token && (
                    <div className="alert alert-info" role="alert">
                        Token: {token}
                    </div>
                )}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            className="form-control"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            className="form-control"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label>Confirm Password</label>
                        <input
                            type="password"
                            className="form-control"
                            name="password2"
                            value={formData.password2}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            className="form-control"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label>First Name</label>
                        <input
                            type="text"
                            className="form-control"
                            name="first_name"
                            value={formData.first_name}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label>Last Name</label>
                        <input
                            type="text"
                            className="form-control"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleChange}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary my-3">
                        Register
                    </button>
                    <p className="mt-3">
                        Already have an account? <Link to="/login">
                        <button className="btn btn-primary">Login</button>
                    </Link>
                    </p>
                </form>
            </div>
        </>
    );
};

export default Register;
