/* checkupdate.js for createupdate.html

Maurice Kingma

Javascript for checking input when editing update
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {

    // select submitbutton
    document.querySelector('[value="save"]').onclick = () => {

        if (document.querySelector('#title').value.length == 0) {
            document.querySelector('#title').setCustomValidity('invalid')
            document.querySelector('#titleHelp').innerHTML = "Geef een titel op"
        } else {
            document.querySelector('#title').setCustomValidity('')
            document.querySelector('#titleHelp').innerHTML = ""

        };
        if (document.querySelector('#date').value.length == 0) {
            document.querySelector('#date').setCustomValidity('invalid')
            document.querySelector('#dateHelp').innerHTML = "Datum mag niet leeg zijn"
        } else {
            document.querySelector('#date').setCustomValidity('')
            document.querySelector('#dateHelp').innerHTML = ""
        };
        if (document.querySelector('#short').value.length == 0) {
            document.querySelector('#short').setCustomValidity('invalid')
            document.querySelector('#shortHelp').innerHTML = "Beschrijving mag niet leeg zijn"
        } else {
            document.querySelector('#short').setCustomValidity('')
            document.querySelector('#shortHelp').innerHTML = ""
        };
        if (document.querySelector('#body').value.length == 0) {
            document.querySelector('#body').setCustomValidity('invalid')
            document.querySelector('#bodyHelp').innerHTML = "'Lees meer' mag niet leeg zijn"
        } else {
            document.querySelector('#body').setCustomValidity('')
            document.querySelector('#bodyHelp').innerHTML = ""
        };
    };
});
