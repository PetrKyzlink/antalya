function getToken(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
	  	var cookies = document.cookie.split(';');
	  	for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
		  	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		  	break;
			}
	  	}
	}
	return cookieValue;
}
var csrftoken = getToken('csrftoken')
var device = getToken('device');



if (device !== null && device !== undefined && device !=="" ){
	var updateBtns = document.getElementsByClassName('update-cart');

	for (i = 0; i < updateBtns.length; i++) {
		updateBtns[i].addEventListener('click', function(){
			
			var action = this.dataset.action;
			if (action == 'add') {
				var productId = this.dataset.product
				console.log('productId:', productId, 'Action:', action)
				updateOrderAdd(productId, action)
			}
			else if (action == 'remove') {
				var cartItemId = this.dataset.cartitem
				console.log('cartItemId:', cartItemId, 'Action:', action)
				updateOrderRemove(cartItemId, action)
			}
			
		})
	}

	function updateOrderAdd(productId, action) {
		var url = "/update_item/";

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({
				"productId": productId, 
				"action": action
			})
		})
		.then((response) => {
			return response.json()
		})
		.then((data) => {
			console.log('Data:', data);
			location.reload()
		})
	}

	function updateOrderRemove(cartItemId, action) {
		var url = '/update_item/';
		fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({
			'cartItemId': cartItemId,
			'action': action
		})
		})
		.then((response) => {
		return response.json();
		})
		.then((data) => {
		console.log('Data:', data);
		location.reload();
		});
	}

	var selDressing = document.getElementsByClassName('get-dressing')

	for (i = 0; i < selDressing.length; i++) {
		selDressing[i].addEventListener('change', function(){
			var cartItemId = this.dataset.cartitem;
			var action = this.dataset.action;
			var selected = this.dataset.selected;
			var dressingId = this.value;
			if (!dressingId) {
				dressingId = 'null'
			}
			
			console.log('cartItemId:', cartItemId, 'Action:', action, 'dressingId:', dressingId, 'selected:', selected) 
			updateDressing(cartItemId, action, dressingId, selected)
		})
	}

	function updateDressing(cartItemId, action, dressingId, selected) {
		var url = '/update_item/';
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
				'cartItemId': cartItemId,
				'action': action,
				'dressingId': dressingId,
				'selected': selected
			})
		})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log('Data:', data);
			location.reload();
		});
	}

	var selDrink = document.getElementsByClassName('get-drink')

	for (i = 0; i < selDrink.length; i++) {
		selDrink[i].addEventListener('change', function(){
			var cartItemId = this.dataset.cartitem;
			var action = this.dataset.action;
			var selected = this.dataset.selected;
			var drinkId = this.value;
			if (!drinkId) {
				drinkId = 'null'
			}
			
			console.log('cartItemId:', cartItemId, 'Action:', action, 'drinkId:', drinkId, 'selected:', selected) 
			updateDrink(cartItemId, action, drinkId, selected)
		})
	}

	function updateDrink(cartItemId, action, drinkId, selected) {
		var url = '/update_item/';
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
				'cartItemId': cartItemId,
				'action': action,
				'drinkId': drinkId,
				'selected': selected
			})
		})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log('Data:', data);
			location.reload();
		});
	}

	var selSideDish = document.getElementsByClassName('get-side-dish')

	for (i = 0; i < selSideDish.length; i++) {
		selSideDish[i].addEventListener('change', function(){
			var cartItemId = this.dataset.cartitem;
			var action = this.dataset.action;
			var selected = this.dataset.selected;
			var sideDishId = this.value;
			if (!sideDishId) {
				sideDishId = 'null'
			}
			
			console.log('cartItemId:', cartItemId, 'Action:', action, 'sideDishId', sideDishId, 'selected:', selected) 
			updateSideDish(cartItemId, action, sideDishId, selected)
		})
	}

	function updateSideDish(cartItemId, action, sideDishId, selected) {
		var url = '/update_item/';
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
				'cartItemId': cartItemId,
				'action': action,
				'sideDishId': sideDishId,
				'selected': selected
			})
		})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log('Data:', data);
			location.reload();
		});
	}
} else {
	// Nothing
}

var linkAlerrgens = document.querySelectorAll('.alerrgens-link');
var alerrgens = document.querySelector('.alerrgens-container');
linkAlerrgens.forEach(function(link) {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    alerrgens.classList.add('show');
  });
});

var closeBtnAlerrgensPage = document.querySelector('.close-alerrgens-page');
if (closeBtnAlerrgensPage) {
	closeBtnAlerrgensPage.addEventListener('click', function(e) {
		e.preventDefault();
		alerrgens.classList.remove('show');
	});
}
var linkTerms = document.querySelectorAll('.terms-link');
var terms = document.querySelector('.terms-container');
linkTerms.forEach(function(link) {
  	link.addEventListener('click', function(e) {
    	e.preventDefault();
    	terms.classList.add('show');
  	});
});

var closeBtnTermsPage = document.querySelector('.close-terms-page');
if (closeBtnTermsPage) {
	closeBtnTermsPage.addEventListener('click', function(e) {
		e.preventDefault();
		terms.classList.remove('show');
	});
}

var linkGDPR = document.querySelectorAll('.gdpr-link');
var gdpr = document.querySelector('.gdpr-container');
linkGDPR.forEach(function(link) {
	link.addEventListener('click', function(e) {
		e.preventDefault();
		gdpr.classList.add('show');
	});
});

var closeBtnGDPRPage = document.querySelector('.close-gdpr-page');
if (closeBtnGDPRPage) {
	closeBtnGDPRPage.addEventListener('click', function(e) {
		e.preventDefault();
		gdpr.classList.remove('show');
	});
}
var linkCookies = document.querySelectorAll('.cookies-link');
var cookies = document.querySelector('.cookies-container');
linkCookies.forEach(function(link) {
  	link.addEventListener('click', function(e) {
    	e.preventDefault();
    	cookies.classList.add('show');
  	});
});

var closeBtnCookiesPage = document.querySelector('.close-cookies-page');
if (closeBtnCookiesPage) {
	closeBtnCookiesPage.addEventListener('click', function(e) {
		e.preventDefault();
		cookies.classList.remove('show');
	});
}

function uuidv4() {
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
		let r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
	return v.toString(16);
	});
}
// Customer changed their mind about cookies
function reCookies() {	
	document.cookie = 'accepted=false;path=/;';
	document.cookie = 'csrftoken=;path=/;expires=0;';
	document.cookie = 'device=;path=/;expires=0;';
	fetch('/reject_cookies/')
		.then(function() {
			location.replace('/nabidka/');
	});
}

function accCookies() {
	device = uuidv4();
	var date = new Date();
	date.setTime(date.getTime() + (14 * 24 * 60 * 60 * 1000)); // 14 dní
	var expires = "; expires=" + date.toUTCString();
	document.cookie = "accepted=true" + expires + ";domain=;path=/";
	document.cookie = "device=" + device + expires + ";domain=;path=/";

	fetch('/accept_cookies/')
		.then(function() {
			location.replace('/nabidka/');
	});

}


