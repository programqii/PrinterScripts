var Enviroment = (function () {
    function Enviroment(isDev) {
        this.isDev = isDev;
    }
    Enviroment.prototype.getPrinterServerEndPoint = function () {
        if (this.isDev == 'true') {
            return 'http:localhost:3000';
        } else {
            return 'http://192.168.1.149:3000';
        }
    };
    return Enviroment;
} ());



/*
var greeter = new Greeter("world");
var button = document.createElement('button');
button.textContent = "Say Hello";
button.onclick = function () {
    alert(greeter.greet());
};
document.body.appendChild(button);

*/