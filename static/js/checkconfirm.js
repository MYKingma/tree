/* checkpost.js for createpost.html

Maurice Kingma

Javascript for checking input when editing post
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {

    // select submitbutton
    document.querySelector('[type="submit"]').onclick = () => {

        if (document.querySelector('#firstname').value.length == 0) {
            document.querySelector('#firstname').setCustomValidity('invalid')
            document.querySelector('#firstnameHelp').innerHTML = "Geef een voornaam op"
        } else {
            document.querySelector('#firstname').setCustomValidity('')
            document.querySelector('#firstnameHelp').innerHTML = ""

        };
        if (document.querySelector('#street').value.length == 0) {
            document.querySelector('#street').setCustomValidity('invalid')
            document.querySelector('#streetHelp').innerHTML = "Geef een straatnaam op"
        } else {
            document.querySelector('#street').setCustomValidity('')
            document.querySelector('#streetHelp').innerHTML = ""
        };
        if (document.querySelector('#number').value.length == 0) {
            document.querySelector('#number').setCustomValidity('invalid')
            document.querySelector('#numberHelp').innerHTML = "Geef een huisnummer op"
        } else {
            document.querySelector('#number').setCustomValidity('')
            document.querySelector('#numberHelp').innerHTML = ""
        };
        if (document.querySelector('#zipcode').value.length == 0) {
            document.querySelector('#zipcode').setCustomValidity('invalid')
            document.querySelector('#zipcodeHelp').innerHTML = "Geef een postcode op"
        } else {
            document.querySelector('#zipcode').setCustomValidity('')
            document.querySelector('#zipcodeHelp').innerHTML = ""
        };
        if (document.querySelector('#location').value.length == 0) {
            document.querySelector('#location').setCustomValidity('invalid')
            document.querySelector('#locationHelp').innerHTML = "Geef een plaatsnaam op"
        } else {
            document.querySelector('#location').setCustomValidity('')
            document.querySelector('#locationHelp').innerHTML = ""
        };
        if (document.querySelector('#lastname').value.length == 0) {
            document.querySelector('#lastname').setCustomValidity('invalid')
            document.querySelector('#lastnamehelp').innerHTML = "Geef een achternaam op"
        } else {
            document.querySelector('#lastname').setCustomValidity('')
            document.querySelector('#lastnamehelp').innerHTML = ""
        };
        if (document.querySelector('#email').value.length == 0) {
            document.querySelector('#email').setCustomValidity('invalid')
            document.querySelector('#emailHelp').innerHTML = "Geef een e-mailadres op"
        } else {
            document.querySelector('#email').setCustomValidity('')
            document.querySelector('#emailHelp').innerHTML = ""
        };
        if (document.querySelector('#email2').value.length == 0) {
            document.querySelector('#email2').setCustomValidity('invalid')
            document.querySelector('#email2Help').innerHTML = "Herhaal het e-mailadres"
        } else {
            document.querySelector('#email2').setCustomValidity('')
            document.querySelector('#email2Help').innerHTML = ""
        };
        if (document.querySelector('#email').value.length > 0 && document.querySelector('#email2').value.length > 0) {
            if (document.querySelector('#email').value == document.querySelector('#email2').value) {
                document.querySelector('#email').setCustomValidity('')
                document.querySelector('#email2').setCustomValidity('')
                document.querySelector('#emailHelp').innerHTML = ""
                document.querySelector('#email2Help').innerHTML = ""
            } else {
                document.querySelector('#email').setCustomValidity('invalid')
                document.querySelector('#email2').setCustomValidity('invalid')
                document.querySelector('#emailHelp').innerHTML = ""
                document.querySelector('#email2Help').innerHTML = "E-mailadressen komen niet overeen"
            }
        }
    };
});
