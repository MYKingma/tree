/* checkpost.js for createpost.html

Maurice Kingma

Javascript for checking input when editing post
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
        if (document.querySelector('#short').value.length == 0) {
            document.querySelector('#short').setCustomValidity('invalid')
            document.querySelector('#shortHelp').innerHTML = "Introductie mag niet leeg zijn"
        } else {
            document.querySelector('#short').setCustomValidity('')
            document.querySelector('#shortHelp').innerHTML = ""
        };
        if (document.querySelector('#body').value.length == 0) {
            document.querySelector('#body').setCustomValidity('invalid')
            document.querySelector('#bodyHelp').innerHTML = "Post mag niet leeg zijn"
        } else {
            document.querySelector('#body').setCustomValidity('')
            document.querySelector('#bodyHelp').innerHTML = ""
        };
    };
});
