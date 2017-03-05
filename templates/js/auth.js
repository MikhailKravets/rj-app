function checkRequired(jElem){
    for(var i = 0; i < jElem.length; i++)
        if(jElem[i].value === '')
            return false;
    return true;
}

function showStatus(jElem, msg){
    jElem.html(msg);
    jElem.css('display', 'block');
}
function hideStatus(jElem){
    jElem.css('display', 'none');
}

function queryServer(url, data, callback){
    $.ajax({
        url: url,
        method: 'POST',
        data: JSON.stringify(data),
        dateType: 'json'
    }).then(function(data){
        callback(data);
    });
}

window.onload = function(){
    var status = $(".statusCode");
    var required = $("[required]");
    
    required.on('keydown', function(e){
        if(e.keyCode === 13)
            $("#signInButton").click();
    });
    
    $("#signInButton").on('click', function(e){
        hideStatus(status);
        if(checkRequired(required)){
            var data = ["LOGIN", $("#name").val(), $("#password").val()]
            queryServer('/auth', data, function(data){
                console.log(data);
                if(data === 'OK'){
                    window.location.replace('/');
                }
                else if(data === 'ERROR'){
                    showStatus(status, "Неправильное сочетание имени и пароля");
                }
            })
            console.log("Plick");
        }
        else{
            console.log("Empty");
            showStatus(status, "Введите имя и пароль для входа в приложение");
        }
    });
}