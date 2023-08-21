import React, { useState } from 'react';
import { Row, Col, Form, FormControl, Button } from 'react-bootstrap';
import { productsArray } from './productsStore';
import ProductCard from './ProductCard';

function Store() {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSearchInputChange = (event) => {
        setSearchQuery(event.target.value);
    };

    const handleSearchSubmit = (event) => {
        event.preventDefault();
        const token = sessionStorage.getItem('authToken');
        if (!token) {
            setError('Authentication token not found.');
            return;
        }

        const searchUrl = `http://localhost:8000/search/?query=${encodeURIComponent(searchQuery)}`;
        fetch(searchUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                setSearchResults(data);
                setError('');
            })
            .catch(error => {
                setError('Error occurred while searching.');
            });
    };

    const displayResults = searchResults.length > 0 ? searchResults : productsArray;

    return (
        <>
            <h1 align="center" className="p-3">Welcome to the Book store!</h1>
            <Form className="d-flex" onSubmit={handleSearchSubmit}>
                <FormControl
                    type="search"
                    placeholder="Search book, author, and genre"
                    className="mr-2"
                    value={searchQuery}
                    onChange={handleSearchInputChange}
                />
                <Button type="submit" variant="outline-success mx-2">
                    Search
                </Button>
            </Form>
            <br/>
            <Row xs={1} md={3} className="g-4">
                {displayResults.map((product, idx) => (
                    <Col align="center" key={idx}>
                        <ProductCard product={product} />
                    </Col>
                ))}
            </Row>
        </>
    );
}

export default Store;
