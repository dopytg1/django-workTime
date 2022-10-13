function onScanSuccess(decodedText, decodedResult) {
    var secret = document.getElementById('secret_key').value;

    if(decodedText == secret){
        const xhr = new XMLHttpRequest();
        var csrfToken = document.getElementById('token').value;  
        var request = document.getElementById('request').value;
        xhr.open("POST", "/accounts/member/create");
        xhr.setRequestHeader('X-CSRFToken', csrfToken)
        xhr.send(request)
        window.location.href = "/accounts/member"
        
    }
}
var html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: 250 });

html5QrcodeScanner.render(onScanSuccess);