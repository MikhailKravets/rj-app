function checkEmail(jElem){
    var pat = /@{1}/;
    for(var i = 0; i < jElem.length; i++)
        if(!pat.test(jElem[i].value))
            return false;
    return true;
}
function checkRequired(jElem){
    for(var i = 0; i < jElem.length; i++)
        if(jElem[i].value === '')
            return false;
    return true;
}

function checkLatin(str){
    pattern = /[^A-Za-z0-9@.]+/i;
    if(pattern.test(str))
        return false;
    else return true;
}

function checkEqual(jElem){
    var val = jElem[0].value;
    for(var i = 1; i < jElem.length; i++)
        if(jElem[i].value !== val)
            return false;
    return true;
}

function showMessage(jElem, msg){
    jElem.html(msg);
    jElem.css('display', 'block');
}
function hideMessage(jElem){
    jElem.css('display', 'none');
}

function queryServer(url, obj, callback){
    $.ajax({
        url: url,
        method: 'POST',
        data: JSON.stringify(obj)
    }).then(function(data){
        callback(data);
    });
}

function quit(){
    $.ajax({
        url: '/',
        method: 'POST',
        data: JSON.stringify(['QUIT'])
    }).then(function(data){
        console.log(data);
        if(data === 'OK')
            window.location.assign('/auth');
    });
}

window.onload = function(e){
    var step = parseInt($("#step").text());
    console.log(step);
    $("#endregButton").on('click', function(e){
        if(step === 1){
            if(!checkRequired($("[required]")))
                showMessage($(".statusCode"), 'Не все поля заполнены');
            else if(!checkEmail($("[email]")) || !checkLatin($("[email]").val()))
                showMessage($(".statusCode"), 'Неправильно введен эл. адрес');
            else {
                hideMessage($(".statusCode"));
                queryServer('/register', ['EMAIL', $("[email]").val()], function(data){
                    data = JSON.parse(data);
                    if(data[0] === 'NEXT'){
                        step++;
                        $("#step").text(step);
                        $("#view").html(data[1]);
                    }
                    else if(data[0] === 'FINISH')
                        window.location.assign('/')
                    else if(data[0] === 'ERROR' && data[1] === 'duplicate')
                        showMessage($(".statusCode"), 'Такой эл. адрес уже зарегистрирован. Попробуйте что-то другое');
                });
            }
        }
        else if(step === 2){
            if(!checkRequired($("[required]")))
                showMessage($(".statusCode"), 'Не все поля заполнены');
            else if(!checkLatin($("#password").val()))
                showMessage($(".statusCode"), 'Используйте только латинские символы и цифры');
            else if(!checkEqual($("[equal]")))
                showMessage($(".statusCode"), 'Введенные пароли не совпадают');
            else {
                hideMessage($(".statusCode"));
                queryServer('/register', ['PASSWORD', $("#password").val()], function(data){
                    data = JSON.parse(data);
                    if(data[0] === 'NEXT'){
                        step++;
                        $("#step").text(step);
                        $("#view").html(data[1]);
                    }
                    else if(data[0] === 'FINISH')
                        window.location.assign('/')
                });
            }
        }
    });
    
    $("#quit").on('click', function(e){
        quit();
    });
}