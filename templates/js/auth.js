function checkRequired(jElem){
    return true;
}


window.onload = function(){
    $("#signInButton").on('click', function(e){
        if(checkRequired($("[required]"))){
            // send data to server
            console.log("Plick");
        }
    });
}