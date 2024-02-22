setInterval(function(){ $(".alert").fadeOut(); }, 3000);

$('#create').on('click', function(){
    console.log(this.id);
    console.log(error);
    if (this.id == "create" && error) {
        sessionStorage.setItem('clicked', 'true');
        sessionStorage.setItem('error', error);
    }
});

let clicked = sessionStorage.getItem('clicked');
let savedError = sessionStorage.getItem('error');
console.log(clicked);
console.log(savedError);

if(clicked === 'true') {
    console.log('got here');
    $("#error-div").css("display", "block");
    $("#error-div").css("visibility", "visible");
    $("#error-div").html(savedError);
    sessionStorage.removeItem('clicked');
    sessionStorage.removeItem('error');
}
