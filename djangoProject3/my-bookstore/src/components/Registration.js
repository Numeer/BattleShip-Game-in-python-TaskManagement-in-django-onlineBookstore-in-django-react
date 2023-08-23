import React, {useState} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import NavBar from './Navbar';
import InputField from './inputField';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        password2: '',
        email: '',
        first_name: '',
        last_name: '',
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
            const response = await axios.post('http://localhost:8000/register/', formData);
            sessionStorage.setItem('authToken', response.data.token);
            sessionStorage.setItem('username', formData.username);
            setToken(response.data.token);
            setSuccess('Registration successful');
            setRedirectToNavbar(true);
        } catch (error) {
            if (error.response) {
                const errorData = error.response.data;
                if (errorData.errors) {
                    setError(Object.values(errorData.errors)[0]); // Display the first error
                } else if (errorData.message) {
                    setError(errorData.message);
                }
            } else {
                setError('No Server Response');
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
                {error && (
                    <div className="alert alert-danger" role="alert">
                        <p>{error}</p>
                    </div>
                )}
                <h2>Register</h2>
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
                    <InputField
                        label="Confirm Password"
                        type="password"
                        name="password2"
                        value={formData.password2}
                        onChange={handleChange}
                    />
                    <InputField
                        label="Email"
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />
                    <InputField
                        label="First Name"
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                    />
                    <InputField
                        label="Last Name"
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                    />
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
