/* shoppingcart.js for shop.html

Maurice Kingma

Javascript for showing shoppingcart
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {

    var orderdict = {}
    document.querySelectorAll('[data-button]').forEach(button => {
        button.onclick = () => {
            var id = button.dataset.button;
            var price = button.dataset.price
            var cartpricediv = document.querySelector('.total');
            var currentamount = parseFloat(cartpricediv.innerHTML.replace('€', ''));
            var amount = 1
            if (price + currentamount > 750) {
                alert("Het maximale totaalbedrag per bestelling is €750,-, dit is de limiet van tikkie betalingen. Wil je meer bestellen? Plaats dan een andere bestelling.")
            } else {
                var name = button.dataset.name;
                var stock = button.dataset.stock;
                button.dataset.stock = stock - 1;
                document.querySelector('[data-currentstock="' + id + '"]').innerHTML = "Voorraad: " + button.dataset.stock;
                if (button.dataset.stock == 0) {
                    var div = document.createElement('DIV');
                    var icon = document.createElement('I');
                    icon.className = "fas fa-check"
                    div.appendChild(icon)
                    div.className = "btn btn-block btn-sm btn-dark btn-green nohover"
                    div.innerHTML = div.innerHTML + " Toegevoegd"
                    button.style.display = "none";
                    button.parentNode.insertBefore(div, button)
                    setTimeout(function(){
                        div.style.display = "none";
                    }, 2000);
                }
                var itemdiv = document.querySelector('.items');
                if (id in orderdict) {
                    var currentamount = parseFloat(cartpricediv.innerHTML.replace('€', ''));
                    cartpricediv.innerHTML = '€' + (currentamount - parseFloat(price * orderdict[id])).toFixed(2);
                    orderdict[id] = parseInt(orderdict[id]) + parseInt(amount)
                    amount = orderdict[id]
                    total = (amount * price).toFixed(2);
                    itemdiv.innerHTML = ""
                } else {
                    orderdict[id] = parseInt(amount)
                };
                pricespan = document.createElement('SPAN');
                pricespan.className = "floatright"
                pricespan.dataset.pricecartid = id;
                pricespan.dataset.pricecart = price * amount;
                pricespan.innerHTML = '€' + (price * amount).toFixed(2);
                item = document.createElement('P');
                item.dataset.itemcartid = id;
                item.innerHTML = amount + 'x ' + name
                item.appendChild(pricespan)
                if (document.querySelector('.empty')) {
                    itemdiv.innerHTML = ""
                }
                itemdiv.appendChild(item);
                var currentamount = parseFloat(cartpricediv.innerHTML.replace('€', ''));
                cartpricediv.innerHTML = '€' + (parseFloat(price * amount) + currentamount).toFixed(2);
                document.querySelector('.emptycart').style.display = "block";
                document.querySelector('.buybutton').disabled = false;
                document.querySelector('.orderdict').value = JSON.stringify(orderdict);
            };
        };
    });

    var empty = document.querySelector('.emptycart').onclick = () => {
        location.reload();
    }
});
