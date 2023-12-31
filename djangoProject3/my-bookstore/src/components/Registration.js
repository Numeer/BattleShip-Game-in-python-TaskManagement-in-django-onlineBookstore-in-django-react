import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import NavBar from './Navbar';
import InputField from './inputField';

const Register = () => {
    const inputFields = [
        {
            label: 'Username',
            type: 'text',
            name: 'username',
        },
        {
            label: 'Password',
            type: 'password',
            name: 'password',
        },
        {
            label: 'Confirm Password',
            type: 'password',
            name: 'password2',
        },
        {
            label: 'Email',
            type: 'email',
            name: 'email',
        },
        {
            label: 'First Name',
            type: 'text',
            name: 'first_name',
        },
        {
            label: 'Last Name',
            type: 'text',
            name: 'last_name',
        },
    ];

    const [formData, setFormData] = useState({});
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
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
            setSuccessMessage('Registration successful');
            setRedirectToNavbar(true);
        } catch (error) {
            if (error.response) {
                const errorData = error.response.data;
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
            {redirectToNavbar && <NavBar />}
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
                    {inputFields.map((field, index) => (
                        <InputField
                            key={index}
                            label={field.label}
                            type={field.type}
                            name={field.name}
                            value={formData[field.name] || ''}
                            onChange={handleChange}
                        />
                    ))}
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
