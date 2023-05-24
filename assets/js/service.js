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

var sendNewOrderConfirmationBtn = document.getElementById('new-order-btn-send-confirmation');
var preparationTime = document.getElementById('get-preparation-time');
if (sendNewOrderConfirmationBtn && preparationTime) {
    sendNewOrderConfirmationBtn.addEventListener('click', function(){
        var orderId = this.dataset.order;
        var minutes = preparationTime.value;

        var url = '/new_order_confirmation/';
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
				'orderId': orderId,
				'minutes': minutes,
			})
		})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log('Data:', data);
			location.replace('/obsluha/#orders-in-process/');
		});
    })
}

var orderCompletedBtn = document.getElementsByClassName('order-completed-btn-send-confirmation');
for (i = 0; i < orderCompletedBtn.length; i++) {
    orderCompletedBtn[i].addEventListener('click', function(){
        var orderId = this.dataset.order;
        var url = '/order_completed/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'orderId': orderId,
            })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data);
            location.replace('/obsluha/');
        });
    })
      
}

var cancellationBtn = document.querySelectorAll('.storno-btn');
cancellationBtn.forEach(function(button) {
    button.addEventListener('click', function() {
        var orderId = this.dataset.order;
        var url = '/order_cancellation/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'orderId': orderId,
            })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data);
            location.replace('/obsluha/');
        });
    })
})  
