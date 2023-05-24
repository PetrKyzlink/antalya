document.addEventListener('DOMContentLoaded', function() {
    var acceptButton = document.querySelector('#accept-cookies');
    var rejectButton = document.querySelector('#reject-cookies');

    acceptButton.addEventListener('click', function() {
        function getToken(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getToken('csrftoken')

        function uuidv4() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                let r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
            });
        }

        let device = getToken('device')

        if (device == null || device == undefined || device =='' ){
            device = uuidv4()
        }

        var date = new Date();
        date.setTime(date.getTime() + (14 * 24 * 60 * 60 * 1000)); 
        var expires = "; expires=" + date.toUTCString();
        document.cookie = "device=" + device + expires + ";domain=;path=/";
        fetch('/accept-cookies/')
            .then(function() {
                document.querySelector('#cookies-banner').remove();
                
            
        });
    });

    rejectButton.addEventListener('click', function() {
        document.cookie = 'cookies_accepted=false;path=/;';
        document.cookie = 'csrftoken=;path=/;expires=0;';
        fetch('/reject-cookies/')
            .then(function() {
                document.querySelector('#cookies-banner').remove();
            });
        });
    });
