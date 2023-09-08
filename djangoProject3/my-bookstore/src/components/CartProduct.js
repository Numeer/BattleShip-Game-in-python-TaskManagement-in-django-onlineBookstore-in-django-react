import { CartContext } from "../context/CartContext";
import { useContext } from "react";
import { getProductData } from "./productsStore";
import { Button, Form, Row, Col } from 'react-bootstrap';

function CartProduct({id, quantity}) {
    const cart = useContext(CartContext);
    const productData = getProductData(id);
    const productQuantity = cart.getProductQuantity(id);
    return (
        <>
            <h3>{productData.title}</h3>
            <p>{quantity} total</p>
            <p>Rs { (quantity * productData.price).toFixed(2) }</p>
            { productQuantity > 0 ?
                    <>
                        <Form as={Row}>
                            <Form.Label column="true" sm="6">In Cart: {productQuantity}</Form.Label>
                            <Col sm="6">
                                <Button sm="6" onClick={() => cart.addOneToCart(id)} className="mx-2">+</Button>
                                <Button sm="6" onClick={() => cart.removeOneFromCart(id)} className="mx-2">-</Button>
                            </Col>
                        </Form>
                    </>
                    :
                    <Button variant="primary" onClick={() => cart.addOneToCart(id)}>Add To Cart</Button>
                }
            <Button size="sm" onClick={() => cart.deleteFromCart(id)}>Remove</Button>
            <hr></hr>
        </>
    )
}


export default CartProduct;