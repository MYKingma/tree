/* background.js for index.html

Maurice Kingma

Javascript for checking and changeing background index.html
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {

	// select checkbox and activate delete button if checked
	if (document.querySelector('.backDrop')) {
		var background = document.querySelector('.backDrop');

	} else {
		var background = document.querySelector('.backDrop2');

	}
	const image = document.querySelector('.backDropLink').dataset.background;
	console.log(image);
	if (image === "None") {

	} else {
		background.style.backgroundImage = 'url(https://raw.githubusercontent.com/MYKingma/tree/master/static/img/' + image + ')';
	}
});
