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

    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
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
        setSuccessMessage('');

        try {
            const response = await axios.post('http://localhost:8000/register/', formData);
            sessionStorage.setItem('authToken', response.data.token);
            sessionStorage.setItem('username', formData.username);
            setToken(response.data.token);
            setSuccessMessage('Registration successful');
            setRedirectToNavbar(true);
        } catch (errorMessage) {
            if (errorMessage.response) {
                const errorData = errorMessage.response.data;
                if (errorData.errors) {
                    setErrorMessage(Object.values(errorData.errors)[0]); // Display the first error
                } else if (errorData.message) {
                    setErrorMessage(errorData.message);
                }
            } else {
                setErrorMessage('No Server Response');
            }
        }
    };

    return (
        <>
            {redirectToNavbar ? <NavBar/> : null}
            <div className="container login-container my-3">
                {successMessage && (
                    <div>
                        <h3 className="text-success">{successMessage}</h3>
                    </div>
                )}
                {errorMessage && (
                    <div className="alert alert-danger" role="alert">
                        <p>{errorMessage}</p>
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
