/* changeprice.js for shop.html

Maurice Kingma

Javascript for showing price at item
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('[data-id]').forEach(field => {
        field.oninput = () => {
            var id = field.dataset.id;
            var pricediv = document.querySelector('[data-priceid="' + id + '"]');
            var amount = field.value;
            var price = pricediv.dataset.price;
            pricediv.innerHTML = '€' + (amount * price).toFixed(2);
        };
    });
});
