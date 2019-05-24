var submitBtn = document.getElementById('load-file-btn');
var urlInput = document.getElementById('input-url');
var badUrlMsg = document.getElementById('bad-url-msg');
var hostAddress = window.location.protocol + '//' + window.location.host;

function isValidURL(str) {
    var pattern = new RegExp('^((ft|htt)ps?:\\/\\/)?'+ // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name and extension
        '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
        '(\\:\\d+)?'+ // port
        '(\\/[-a-z\\d%@_.~+&:]*)*'+ // path
        '(\\?[;&a-z\\d%@_.,~+&:=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
    return pattern.test(str);
}

submitBtn.addEventListener('click', function(event) {
    event.preventDefault();
    badUrlMsg.hidden = true;
    var input_url = urlInput.value;

    if (!isValidURL(input_url)) {
        badUrlMsg.hidden = false;
        badUrlMsg.textContent = "I can't shorten: Not a valid URL";
        return;
    }

    if (input_url.startsWith(hostAddress)) {
        badUrlMsg.hidden = false;
        badUrlMsg.textContent = "I can't shorten: This is my link";
        return;
    }

    if (!input_url.startsWith('http://') && !input_url.startsWith('https://')) {
        input_url = 'http://' + input_url;
    }

    var headers = new Headers();
    headers.set('Accept', 'application/json');
    var formData = new FormData();
    formData.append('input_url', input_url);

    var url = '/link/shorten';
    var fetchOptions = {
        method: 'POST',
        headers,
        body: formData
    };

    fetch(url, fetchOptions)
    .then(function(response) {
        return response.json();
    })
    .then(function(jsonData) {
        document.getElementById('input-url').value = 
        hostAddress + '/' + jsonData['short'];
    });
});