const scanner = new Html5QrcodeScanner('scan-reader', {
    qrbox: {
        width: 1000,
        height: 1000,
    },
    fps: 5,
});
scanner.render(success, error);

function success(result) {

    // document.getElementById('result').innerHTML = `<h1 class="text-lg lg:text-2xl uppercase font-bold text-center">Success : ${result}</h1>`;
    // document.getElementById('result').value = result;
    // scanner.clear();
    // document.getElementById('scan-reader').remove();
    // document.getElementById('qr-form').submit();
    
    const baseUrl = 'https://esummit.edcnitd.co.in/qr/scan/';
    
    if (result.startsWith(baseUrl)) {
        const uniqueCode = result.substring(baseUrl.length).split('/')[0];
        window.location.href = `/qr/scan/${uniqueCode}`;
    }
}

function error(error) {
    console.error(error);
}