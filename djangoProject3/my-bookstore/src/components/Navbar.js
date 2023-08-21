// import React, {Component} from 'react';
// import {Navbar, Nav, Container, Form, Button, FormControl} from 'react-bootstrap';
// import {Link} from 'react-router-dom';
//
// class NavBar extends Component {
//     constructor(props) {
//         super(props);
//         this.state = {
//             searchQuery: '',
//             searchResults: [],
//         };
//     }
//
//     handleSearchInputChange = (event) => {
//         this.setState({
//             searchQuery: event.target.value,
//         });
//     };
//
//     handleSearchSubmit = (event) => {
//         event.preventDefault();
//         const {searchQuery} = this.state;
//         const token = sessionStorage.getItem('authToken'); // Get the authentication token
//         if (!token) {
//             console.error('Authentication token not found.');
//             return;
//         }
//
//         const searchUrl = `http://localhost:8000/search/?query=${encodeURIComponent(searchQuery)}`;
//         fetch(searchUrl, {
//             method: 'GET',
//             headers: {
//                 'Authorization': `Token ${token}`, // Include the authentication token
//                 'Content-Type': 'application/json',
//             },
//         })
//             .then(response => response.json())
//             .then(data => {
//                 this.setState({
//                     searchResults: data,
//                 })
//                 console.log('Search results:', data);
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//     };
//
//     render() {
//         const {searchQuery, searchResults} = this.state;
//         return (
//             <Navbar bg="dark" variant="dark" expand="lg">
//                 <Container>
//                     <Navbar.Brand as={Link} to="/books">
//                         Bookstore
//                     </Navbar.Brand>
//                     <Navbar.Toggle aria-controls="basic-navbar-nav"/>
//                     <Navbar.Collapse id="basic-navbar-nav">
//                         <Nav className="me-auto">
//                             <Nav.Link as={Link} to="/books">
//                                 Books
//                             </Nav.Link>
//                             <Nav.Link as={Link} to="/cartitems">
//                                 Cart
//                             </Nav.Link>
//                         </Nav>
//                         <Form className="d-flex" onSubmit={this.handleSearchSubmit}>
//                             <FormControl
//                                 type="search"
//                                 placeholder="Search book,author and genre"
//                                 className="mr-2"
//                                 value={searchQuery}
//                                 onChange={this.handleSearchInputChange}
//                             />
//                             <Button type="submit" variant="outline-success mx-2">
//                                 Search
//                             </Button>
//                         </Form>
//                         <Nav>
//                             <Nav.Link as={Link} to="/user">
//                                 Profile
//                             </Nav.Link>
//                         </Nav>
//                     </Navbar.Collapse>
//                 </Container>
//             </Navbar>
//         );
//     }
// }
//
// export default NavBar;

import React from 'react';
import {Navbar, Nav, Container, Button, Modal} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {useState, useContext} from 'react';
import {CartContext} from "./CartContext";
import CartProduct from './CartProduct';
import {  getProductData } from "./productsStore";

function NavBar() {
    const cart = useContext(CartContext);
    const productsCount = cart.items.reduce((sum, product) => sum + product.quantity, 0);
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [totalPrice, setTotalPrice] = useState(0);
    let productData=[];
    let ID=[]
    const checkout = async () => {
        let totalPrice=0;
        for (const item of cart.items) {
            productData = getProductData(item.id);
            totalPrice += productData.price * item.quantity;
            ID = productData.Id
        }
        setTotalPrice(totalPrice);
        const authToken =  sessionStorage.getItem('authToken');
        const username = sessionStorage.getItem('username');
        await fetch('http://127.0.0.1:8000/checkout/', {
            method: "POST",
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({items: cart.items,username: username,bookId: ID, total_price: totalPrice})
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
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Shopping Cart</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {productsCount > 0 ?
                        <>
                            <p>Items in your cart:</p>
                            {cart.items.map((currentProduct, idx) => (
                                <CartProduct key={idx} id={currentProduct.id}
                                             quantity={currentProduct.quantity}></CartProduct>
                            ))}

                            <h1>Total: {cart.getTotalCost().toFixed(2)}</h1>

                            <Button variant="success" onClick={checkout}>
                                Purchase items!
                            </Button>
                        </>
                        :
                        <h1>There are no items in your cart!</h1>
                    }
                </Modal.Body>
            </Modal>
        </>
    );
}

export default NavBar;