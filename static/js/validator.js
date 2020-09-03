/* validator.js

Maurice Kingma

Javascript for checking input (bootstrap validator)
*/

(function() {
  'use strict';
  document.addEventListener('DOMContentLoaded', function() {
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.stopPropagation();
		  event.preventDefault();
	  } else {

	  }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
