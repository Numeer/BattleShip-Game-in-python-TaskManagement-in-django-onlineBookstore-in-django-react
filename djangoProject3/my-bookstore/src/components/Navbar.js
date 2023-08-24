import React from 'react';
import {Navbar, Nav, Container, Button, Modal} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {useState, useContext} from 'react';
import {CartContext} from "../context/CartContext";
import CartModalContent from './CartModalContent';
import {getProductData} from "./productsStore";

function NavBar() {
    const cart = useContext(CartContext);
    const productsCount = cart.items.reduce((sum, product) => sum + product.quantity, 0);
    const [showDialog, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [totalPrice, setTotalPrice] = useState(0);

    let productData = [];
    let bookIDs = []
    const checkout = async () => {
        let totalPrice = 0;
        for (const item of cart.items) {
            productData = getProductData(item.id);
            totalPrice += productData.price * item.quantity;
            bookIDs.push(productData.Id);
        }
        setTotalPrice(totalPrice);
        const authToken = sessionStorage.getItem('authToken');
        const username = sessionStorage.getItem('username');
        await fetch('http://127.0.0.1:8000/checkout/', {
            method: "POST",
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({items: cart.items, username: username, bookId: bookIDs, total_price: totalPrice})
        }).then((response) => {
            return response.json();
        }).then((response) => {
            if (response.url) {
                window.location.assign(response.url);
            }
        });
    }
    return (
        <>
            <Navbar bg="dark" variant="dark" expand="lg">
                <Container>
                    <Navbar.Brand as={Link} to="/books">
                        Bookstore
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            <Nav.Link as={Link} to="/books">
                                Books
                            </Nav.Link>

                        </Nav>
                        <Nav>
                            <Nav.Link as={Link} to="/user">
                                Profile
                            </Nav.Link>
                            <Navbar.Collapse className="justify-content-end">
                                <Button className="btn btn-link" style={{textDecoration: 'none', color: 'white'}}
                                        onClick={handleShow}>Cart ({productsCount} Items)</Button>
                            </Navbar.Collapse>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
            <Modal show={showDialog} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Shopping Cart</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <CartModalContent cart={cart} checkout={checkout}/>
                </Modal.Body>
            </Modal>
        </>
    );
}


export default NavBar;