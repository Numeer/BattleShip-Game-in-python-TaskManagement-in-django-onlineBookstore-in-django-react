import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import {Button} from "react-bootstrap";
import {CartContext} from "./CartContext";
import {useContext} from "react";

function BookDetail() {
    const [book, setBook] = useState(null);
    const [ratings, setRatings] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [error, setError] = useState(null);
    const [userRating, setUserRating] = useState(0);
    const [userReview, setUserReview] = useState('');
    const cart = useContext(CartContext);

    const {bookId} = useParams();
    useEffect(() => {
            async function fetchBook() {
                try {
                    const token = sessionStorage.getItem('authToken');
                    if (!token) {
                        setError('Authentication token not found.');
                        return;
                    }

                    const bookUrl = `http://localhost:8000/books/${bookId}/`;
                    const ratingsUrl = `http://localhost:8000/ratings/?book=${bookId}/`;
                    const reviewsUrl = `http://localhost:8000/reviews/?book=${bookId}/`;

                    const bookResponse = await fetch(bookUrl, {
                        method: 'GET', headers: {
                            'Authorization': `Token ${token}`, 'Content-Type': 'application/json',
                        },
                    });

                    const ratingsResponse = await fetch(ratingsUrl, {
                        method: 'GET', headers: {
                            'Authorization': `Token ${token}`, 'Content-Type': 'application/json',
                        },
                    });

                    const reviewsResponse = await fetch(reviewsUrl, {
                        method: 'GET', headers: {
                            'Authorization': `Token ${token}`, 'Content-Type': 'application/json',
                        },
                    });

                    if (bookResponse.ok && ratingsResponse.ok && reviewsResponse.ok) {
                        const bookData = await bookResponse.json();
                        const ratingsData = await ratingsResponse.json();
                        const reviewsData = await reviewsResponse.json();
                        setBook(bookData);
                        setRatings(ratingsData);
                        setReviews(reviewsData);
                        const userRatingData = ratingsData.find(rating => rating.user === sessionStorage.getItem('username'));
                        if (userRatingData) {
                            setUserRating(userRatingData.rating);
                        }
                    } else {
                    }
                } catch
                    (error) {
                }
            }

            fetchBook();
        },
        [bookId]
    )
    ;
    const totalRating = ratings.reduce((sum, rating) => sum + rating.rating, 0);
    const averageRating = totalRating / ratings.length;

    const handleRatingChange = async (newRating) => {
        setUserRating(newRating);

        try {
            const token = sessionStorage.getItem('authToken');
            if (!token) {
                setError('Authentication token not found.');
                return;
            }

            const ratingData = {
                user: sessionStorage.getItem('username'), book: book.title, rating: newRating,
            };

            const response = await fetch(`http://localhost:8000/ratings/?book=${bookId}`, {
                method: 'POST', headers: {
                    'Authorization': `Token ${token}`, 'Content-Type': 'application/json',
                }, body: JSON.stringify(ratingData),
            });
            if (response.ok) {
                window.location.reload();
            }

        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleReviewSubmit = async (e) => {
        e.preventDefault();

        try {
            const token = sessionStorage.getItem('authToken');
            if (!token) {
                setError('Authentication token not found.');
                return;
            }


            const reviewData = {
                user: sessionStorage.getItem('username'), book: book.title, text: userReview,
            };

            const response = await fetch(`http://localhost:8000/reviews/?book=${bookId}`, {
                method: 'POST', headers: {
                    'Authorization': `Token ${token}`, 'Content-Type': 'application/json',
                }, body: JSON.stringify(reviewData),
            });
            if (response.ok) {
                setUserReview('');
                window.location.reload();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    const handleReviewDelete = async (reviewId) => {
        try {
            const token = sessionStorage.getItem('authToken');
            if (!token) {
                setError('Authentication token not found.');
                return;
            }

            const response = await fetch(`http://localhost:8000/reviews/${reviewId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                },
            });

            if (response.ok) {
                setReviews(reviews.filter(review => review.id !== reviewId));
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    const generateStars = (rating) => {
        const stars = [];
        for (let i = 1; i <= 5; i++) {
            const starClass = i <= rating ? 'star filled' : 'star';
            stars.push(<span
                key={i}
                className={starClass}
                onClick={() => handleRatingChange(i)}
            >
                    ★
                </span>);
        }
        return stars;
    };

    return (<div className="container my-3">
        {error ? (<div className="alert alert-danger">{error}</div>) : (<div>
            <h2>Book Detail</h2>
            {book && (<div>
                <h3>{book.title}</h3>
                <strong>By:</strong> {book.author}<br/>
                <strong>Genre:</strong> {book.genres.join(', ')}<br/>
                <strong>Rs:</strong> {book.price} <br/>
                <strong>Ratings:</strong> {averageRating.toFixed(2)}
                <Button className="btn btn-primary mx-3" onClick={() => cart.addOneToCart(book.price_id)}>Add To
                    Cart</Button>
            </div>)}
            <h5>Add Your Review:</h5>
            <form onSubmit={handleReviewSubmit}>
                <div className="mb-3">
                    <textarea
                        className="form-control"
                        rows="4"
                        placeholder="Write your review..."
                        value={userReview}
                        onChange={(e) => setUserReview(e.target.value)}
                    ></textarea>
                </div>
                <button type="submit" className="btn btn-primary">
                    Submit Review
                </button>
            </form>
            <h5>Your Rating:</h5>
            <div className="rating-stars">
                {generateStars(userRating)}

            </div>
            <h5>Customer Reviews:</h5>
            {reviews.length > 0 ? (<ul>
                {reviews.map(review => (
                    <li key={review.id}>
                        {review.user}{": "} {review.text}
                        {review.user === sessionStorage.getItem('username') && (
                            <button type="button" className="btn btn-link"
                                    onClick={() => handleReviewDelete(review.id)}><span className="bi bi-trash "></span>
                            </button>
                        )}
                    </li>
                ))}
            </ul>) : (<p>No reviews available.</p>)}
            <style>
                {`
                                .star {
                                color: gray; 
                                cursor: pointer;
                                }

                                .star.filled {
                                 color: yellow; 
                                }
                             `}
            </style>
        </div>)}
    </div>);
}

export default BookDetail;
