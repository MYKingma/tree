/* copylink.js for createupdate.html and createpost.html

Maurice Kingma

Javascript for copying image link
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('NewLinks', () => {

        // select all link buttons
        document.querySelectorAll('#sPath').forEach(link => {
            link.onclick = () => {
                navigator.clipboard.writeText(link.dataset.link);
                link.childNodes[0].className = "fas fa-check"
                setTimeout(function(){
                    link.childNodes[0].className = "fas fa-copy"
                }, 2000);

            };
        });
    });
});
