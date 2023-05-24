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
if (device !== null && device !== undefined){
	var selectDelivery = document.getElementsByClassName('get-delivery');

	for (i = 0; i < selectDelivery.length; i++) {
		selectDelivery[i].addEventListener('change', function(){
			var orderId = this.dataset.order;
			var deliveryId = this.value;
			if (!deliveryId) {
				deliveryId = 'null'
			}
			
			console.log('orderId:', orderId, 'deliveryId', deliveryId) 
			updateDelivery(orderId, deliveryId)
		})
	}

	function updateDelivery(orderId, deliveryId) {
		var url = '/update_delivery/';
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
				'deliveryId': deliveryId,
				'orderId': orderId,
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

	function numberOfCharacterComment() {
		var number = document.getElementById('customer-comment').value.length;
		var remainsNumber = 1000 - number;
		var numberCharacter = document.getElementById('number-of-character');
		numberCharacter.innerHTML = remainsNumber + "/1000";
	}

	var totalPriceWithDeliveryElement = document.getElementById("get-total-price-with-delivery");
	var totalPriceWithDelivery = totalPriceWithDeliveryElement.innerText;


	var sendOrderButton = document.getElementById('send-order');
	sendOrderButton.style.display= 'none';
	var sendOrderButtonPlaceWithoutCustomerData = document.getElementById('send-order__place-without-customer-data');

	for (var i = 0; i < selectDelivery.length; i++) {
		if (selectDelivery[i].value === "") {
			sendOrderButton.style.display= 'none';
		}
	}

	var customerName = document.getElementById('name');
	var customerLastName = document.getElementById('last-name');
	var customerEmail = document.getElementById('email');
	var customerPhone = document.getElementById('phone');
	var customerConsentsTerms = document.getElementById('consent-to-terms');
	var customerConsentsGDPR = document.getElementById('consent-to-gdpr');
	var customerComment = document.getElementById('customer-comment');

	if (customerName !== null && customerLastName!== null && customerEmail !== null && customerPhone !== null) {
		customerName.addEventListener('input', checkCustomerFormValidity);
		customerLastName.addEventListener('input', checkCustomerFormValidity);
		customerEmail.addEventListener('input', checkCustomerFormValidity);
		customerPhone.addEventListener('input', checkCustomerFormValidity);
		customerConsentsTerms.addEventListener('input', checkCustomerFormValidity);
		customerConsentsGDPR.addEventListener('input', checkCustomerFormValidity);
		customerComment.addEventListener('input', checkCustomerFormValidity);
	} 


	var customerAddressStreet = document.getElementById('street');
	var customerAddressCity = document.getElementById('city');
	var customerAddressZipcode = document.getElementById('zipcode');
	if (customerAddressStreet !== null && customerAddressCity !== null && customerAddressZipcode !== null) {
		customerAddressStreet.addEventListener('input', checkCustomerFormValidity);
		customerAddressCity.addEventListener('input', checkCustomerFormValidity);
		customerAddressZipcode.addEventListener('input', checkCustomerFormValidity);
	}

	function checkCustomerFormValidity() {
		const invalidChars = ["'", ":", ";", "#", "\\", "%", "*", "(", ")", "/", "[", "]", "="];
		const invalidCharsComment = ["'", ";", "#", "\\", "%", "*", "(", ")", "/", "[", "]", "="];
		const phoneRegex = /^(\+?\d{1,3}\s?)?(\d[\s-]?){8,20}\d$/;
		const zipcodeRegex = /^\d{3}\s?\d{2}$|^\d{5}$/;
		var isValid = true;
		

		if (customerName.value.length === 0 || customerName.value.length >= 50 || invalidChars.some(char => customerName.value.includes(char))) {
			isValid = false;
		}	
		
		if (customerLastName .value.length === 0 || customerLastName .value.length >= 50 || invalidChars.some(char => customerLastName .value.includes(char))) {
			isValid = false;
		}
			
		if (customerEmail.value.length === 0 || customerEmail.value.length >= 80 || invalidChars.some(char => customerEmail.value.includes(char)) || !customerEmail.value.includes('@')) { 
			isValid = false;
		}
		
		if (!phoneRegex.test(customerPhone.value)) {
			isValid = false;
		}
		
		if (customerAddressStreet !== null && customerAddressCity !== null && customerAddressZipcode !== null) {
			if (customerAddressStreet.value.length === 0 || customerAddressStreet.value.length >= 80 || invalidChars.some(char => customerAddressStreet.value.includes(char))) {
				isValid = false;
			}
			if (customerAddressCity.value.length === 0 || customerAddressCity.value.length >= 80 || invalidChars.some(char => customerAddressCity.value.includes(char))) {
				isValid = false;
			}
			
			if (!zipcodeRegex.test(customerAddressZipcode.value)) {
				isValid = false;
			}
		}

		if (!customerConsentsTerms.checked) {
			isValid = false;
		}
		if (!customerConsentsGDPR.checked) {
			isValid = false;
		}

		if (customerComment.value.length >= 1000 || invalidCharsComment.some(char => customerComment.value.includes(char))) {
			isValid = false;
		}

		if (isValid) {
			sendOrderButton.style.display = 'flex';
			sendOrderButtonPlaceWithoutCustomerData.style.display = 'none';
		} else {
			sendOrderButton.style.display = 'none';
		}
		
	}

	sendOrderButton.addEventListener('click', function(e) {
		submitUserFormData();
	});

	var customerForm = document.getElementById('checkout-customer-form');

	customerForm.addEventListener('submit', function(e){	
		e.preventDefault()
		console.log('Form Submitted.')
	})


	function submitUserFormData() {
		console.log('Send order button clicked');

		var customerName = customerForm.name.value;
		var customerLastName = customerForm.last_name.value;
		var customerEmail = customerForm.email.value;
		var customerPhone = customerForm.phone.value;

		var customerAddressStreetElement = document.getElementById('street');
		var customerAddressCityElement = document.getElementById('city');
		var customerAddressZipcodeElement = document.getElementById('zipcode');
		if (customerAddressStreetElement !== null && customerAddressCityElement !== null && customerAddressZipcodeElement !== null) {
			customerAddressStreet = customerForm.street.value;
			customerAddressCity = customerForm.city.value;
			customerAddressZipcode = customerForm.zipcode.value;
		}
		var customerConsentsTerms = customerForm.consent_to_terms.checked;
		var customerConsentsGDPR = customerForm.consent_to_gdpr.checked;

		var customerComment = customerForm.customer_comment.value;
		if (!customerComment) {
			customerComment = null;
		}

		var customerFormData = {
			'name': customerName,
			'lastName': customerLastName,
			'email': customerEmail,
			'phone': customerPhone,
			'comment': customerComment,
			'consentsToTerms': customerConsentsTerms,
			'consentsToGDPR': customerConsentsGDPR,
			'totalPrice': totalPriceWithDelivery,
		};

		if (customerAddressStreetElement !== null && customerAddressCityElement !== null && customerAddressZipcodeElement !== null) {
			customerFormData.street = customerAddressStreet;
			customerFormData.city = customerAddressCity;
			customerFormData.zipcode = customerAddressZipcode;
		}
		console.log("User info: ", customerFormData);
		
		var url = '/objednavka/';
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
				'customerData': customerFormData,
			})
		})
		.then((response) => {
			if (response.status === 200) {
				return response.url;
			}
		})
		.then((data) => {
			console.log('Data:', data);
			if (typeof data === "string") {
				window.location.href = data;
			}
		});
	}
} else {
	// Nothing
}