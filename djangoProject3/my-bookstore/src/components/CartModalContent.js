import React from 'react';
import CartProduct from './CartProduct';
import { Button } from 'react-bootstrap';

function CartModalContent({ cart, checkout }) {
    const productsCount = cart.items.reduce((sum, product) => sum + product.quantity, 0);

    return (
        <>
            {productsCount > 0 ?
                <>
                    <p>Items in your cart:</p>
                    {cart.items.map((currentProduct, idx) => (
                        <CartProduct key={idx} id={currentProduct.id} quantity={currentProduct.quantity} />
                    ))}

                    <h2>Total Rs: {cart.getTotalCost().toFixed(2)}</h2>

                    <Button variant="success" onClick={checkout}>
                        Purchase items!
                    </Button>
                </>
                :
                <h1>There are no items in your cart!</h1>
            }
        </>
    );
}

export default CartModalContent;
