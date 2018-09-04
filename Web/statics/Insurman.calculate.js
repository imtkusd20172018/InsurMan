function calculateIRR() {
            var yearInput = document.getElementById('yearInput').value;
            var depositInput = document.getElementById('depositInput').value;
            var receiveInput = document.getElementById('receiveInput').value;

            var IRRvalue = (Math.pow((receiveInput / depositInput), (1 / yearInput))) - 1;

            var strOutput =  String(IRRvalue.toFixed(2) * 100) + "%";
            document.getElementById('IRROutput').innerHTML = strOutput;
        }