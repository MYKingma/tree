/* showitems.js

Maurice Kingma

Javascript for showing divs
*/

function showItems(category) {
	console.log(category);
	var hide = document.querySelector('.show')
	if (hide) {
		hide.className = "hide";
	}
	var show = document.querySelector(`[data-category='${category}'`)
	show.className = "show"
	zenscroll.to(show)
}
