import React, { useState, useEffect } from 'react';
import axios  from "axios";
function UserList() {
    const [users, setUsers] = useState([]);
    const [orderData, setOrderData] = useState(null);
    const [orderIdInput, setOrderIdInput] = useState('');
    const [orderNotFound, setOrderNotFound] = useState(false);
    const token = sessionStorage.getItem('authToken');

    useEffect(() => {
        if (!token) {
            return;
        }
        axios.get('http://localhost:8000/user/', {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.data)
            .then(data => {
                setUsers(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }, [token]);

    const handleViewOrder = () => {
        if (orderIdInput === '') {
            alert('Please enter an order ID.');
            return;
        }

        axios.get(`http://127.0.0.1:8000/order/${orderIdInput}/`, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`
            }
        })
            .then(response => {
                if (response.status === 404) {
                    setOrderNotFound(true);
                    return null;
                }
                else if (response.status === 401)
                {
                    setOrderNotFound(true);
                    return null;
                }
                return response.data;
            })
            .then(orderData => {
                if (orderData) {
                    setOrderData(orderData);
                    setOrderNotFound(false);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };
    const handleLogout = () => {
        sessionStorage.removeItem('authToken');
        window.location.assign('/login')
    };

    return (
        <div className="container">
            <h1 className="my-4">User Profile</h1>
            <ul className="list-group">
                {users.map(user => (
                    <li key={user.id} className="list-group-item">
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>First Name:</strong> {user.first_name}</p>
                        <p><strong>Last Name:</strong> {user.last_name}</p>
                        <div>
                            <input
                                type="text"
                                placeholder="Enter Order ID"
                                value={orderIdInput}
                                onChange={e => setOrderIdInput(e.target.value)}
                            />
                            <button onClick={handleViewOrder}>View Order</button>
                        </div>
                        {orderData && (
                            <div>
                                <p>Your order status is {orderData.status}</p>
                            </div>
                        )}
                        {orderNotFound && (
                            <div>
                                <p>No order found with such ID.</p>
                            </div>
                        )}
                        <button className="btn btn-dark my-3" onClick={handleLogout}>Logout</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}


export default UserList;
