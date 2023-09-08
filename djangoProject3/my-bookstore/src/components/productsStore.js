const url = "http://localhost:8000/books/";
const authToken =  sessionStorage.getItem('authToken');
let productsArray = [];

const fetchOptions = {
  headers: {
    Authorization: `token ${authToken}`
  }
};


if (authToken) {
  fetch(url, fetchOptions)
    .then(response => response.json())
    .then(data => {
      productsArray = data.map(item => ({
        id: item.price_id,
        title: item.title,
        price: item.price,
        author: item.author,
        genre: item.genres,
        Id: item.id
      }));
    });
}

function getProductData(id) {
    let productData = productsArray.find(product => product.id === id);
    if (productData === undefined) {
        return undefined;
    }

    return productData;
}


export { productsArray, getProductData };
