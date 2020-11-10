/* lockradio.js

Maurice Kingma

Javascript for locking radiobutton
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {
	// select checkbox and activate delete button if checked
	document.querySelectorAll('#radioinput').forEach(radio => {
		radio.oninput = () => {
			var value = radio.dataset.pos;
			console.log(value);
			var radios = document.querySelectorAll(`[data-pos='${value}'`)
			for (var i = 0; i < radios.length; i++) {
				if (!radios[i].checked && radios[i].type == "radio") {
					radios[i].disabled = true;
				};
			};
			var selectedstring = ""
			var radios = document.querySelectorAll(`[type='radio'`)
			for (var i = 0; i < radios.length; i++) {
				if (radios[i].checked) {
					selectedstring = selectedstring + radios[i].dataset.pos
				}
			}
			if (!selectedstring.includes(1)) {
				for (var i = 0; i < radios.length; i++) {
					if (radios[i].dataset.pos == 1) {
						radios[i].disabled = false;
					}
				}
			}
			if (!selectedstring.includes(2)) {
				for (var i = 0; i < radios.length; i++) {
					if (radios[i].dataset.pos == 2) {
						radios[i].disabled = false;
					}
				}
			}
			if (!selectedstring.includes(3)) {
				for (var i = 0; i < radios.length; i++) {
					if (radios[i].dataset.pos == 3) {
						radios[i].disabled = false;
					}
				}
			}
		};
	});
});
