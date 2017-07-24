function fajs(){
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       document.getElementById("zip_code").innerHTML = xhttp.responseText;
    }
};
xhttp.open("GET", "chooseoutfit.html", true);
xhttp.send();
}
