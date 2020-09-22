/* myorder.js for myorder.html

Maurice Kingma
Minor Programmeren - Web App Studio

Javascript for updating myorder page with progress

*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {


	// create websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	// wait for new progress
	socket.on('refresh', data => {

		// close socket and reload page
		socket.close();
		location.reload();
	});
});

// close socket before leaving page
document.addEventListener('beforeunload', () => {
	socket.close();
});
