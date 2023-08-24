import {Card, Button,} from 'react-bootstrap';
import {CartContext} from '../context/CartContext';
import {useContext} from 'react';
import {Link} from "react-router-dom";
import "../styles.css"
function ProductCard(props) {

    const product = props.product;
    const cart = useContext(CartContext);
       return (
        <Card className="product-card">
            <Card.Body>
                <Card.Title>{product.title}</Card.Title>
                <Card.Text className="price">Price Rs: {product.price}</Card.Text>
                <Card.Text className="genre">{product.genre}</Card.Text>
                <Card.Text className="author">By {product.author}</Card.Text>
                <Link to={`/books/${product.Id}`} className="btn btn-primary view-details">View Details
                </Link>
                <br/>
                <Button
                    className="btn btn-primary my-2 add-to-cart"
                    onClick={() => cart.addOneToCart(product.id)}>Add To Cart
                </Button>
            </Card.Body>
        </Card>
    );
}


export default ProductCard;
