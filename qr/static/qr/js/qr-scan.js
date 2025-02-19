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
    console.log(result)
    window.location.href = `scan/${result}`;
}

function error(error){
}