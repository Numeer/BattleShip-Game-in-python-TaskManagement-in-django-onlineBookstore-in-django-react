import {Card, Button,} from 'react-bootstrap';
import {CartContext} from './CartContext';
import {useContext} from 'react';
import {Link} from "react-router-dom";

function ProductCard(props) {
    const product = props.product;
    const cart = useContext(CartContext);
    return (
        <Card>
            <Card.Body>
                <Card.Title>{product.title}</Card.Title>
                <Card.Text>Price Rs: {product.price}</Card.Text>
                <Card.Text>{product.genre}</Card.Text>
                <Card.Text>{product.author}</Card.Text>
                <Link to={`/books/${product.Id}`} className="btn btn-primary">
                    View Details
                </Link>
                <Button className="btn btn-primary mx-3" onClick={() => cart.addOneToCart(product.id)}>Add To Cart</Button>
            </Card.Body>
        </Card>
    )
}

export default ProductCard;