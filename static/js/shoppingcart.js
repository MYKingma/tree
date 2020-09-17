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
            var amount = document.querySelector('[data-id="' + id + '"]').value;
            var pricediv = document.querySelector('[data-priceid="' + id + '"]')
            var price = pricediv.dataset.price
            var total = (amount * price).toFixed(2);
            var cartpricediv = document.querySelector('.total');
            var currentamount = parseFloat(cartpricediv.innerHTML.replace('€', ''));
            if (total + currentamount > 750) {
                alert("Het maximale totaalbedrag per bestelling is €750")
            } else {
                var name = pricediv.dataset.name;
                document.querySelector('[data-id="' + id + '"]').value = 0
                pricediv.innerHTML = '€0.00'
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
                pricespan.dataset.pricecart = total;
                pricespan.innerHTML = '€' + total;
                item = document.createElement('P');
                item.dataset.itemcartid = id;
                item.innerHTML = amount + 'x ' + name
                item.appendChild(pricespan)
                if (document.querySelector('.empty')) {
                    itemdiv.innerHTML = ""
                }
                itemdiv.appendChild(item);
                var currentamount = parseFloat(cartpricediv.innerHTML.replace('€', ''));
                cartpricediv.innerHTML = '€' + (parseFloat(total) + currentamount).toFixed(2);
                document.querySelector('.emptycart').style.display = "block";
                document.querySelector('.buybutton').disabled = false;
                document.querySelector('.orderdict').value = JSON.stringify(orderdict);
            };
        };
    });

    var empty = document.querySelector('.emptycart').onclick = () => {
        orderdict = {}
        emptytext = document.createElement("P");
        emptytext.innerHTML = "De winkelwagen is nog leeg"
        emptytext.className = "empty"
        document.querySelector('.items').innerHTML = "";
        document.querySelector('.items').appendChild(emptytext);
        document.querySelector('.total').innerHTML = "€0.00"
        document.querySelector('.emptycart').style.display = "none";
        document.querySelector('.buybutton').disabled = true;
    }

});
