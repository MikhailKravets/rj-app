function Controller(){
    var model = {
        'login': '',
        'first': '',
        'middle': '',
        'last': '',
        'access': '',
        'sex': ''
    };
    
    initModel(model);
    
    $("[latin]").on('blur', function(e){
        if(e.target.value !== ''){
            if(!checkLatin(e.target.value)){
                showMessage($(".message"), 'В ник-нейме допустимо использовать только латинские символы и цифры');
            }
            else {
                hideMessage($(".message"));
            }
        }
        else hideMessage($(".message"));
    });
    $("[numeric]").on('blur', function(e){
        if(e.target.value !== ''){
            console.log(checkNumeric(e.target.value));
            if(!checkNumeric(e.target.value))
                showMessage($(".message"), 'Здесь можно ввести всего несколько цифр подряд. Я же Вам, кажется, даже говорил какие!?');
            else hideMessage($(".message"));
        }
        else hideMessage($(".message"));
    });
    $("[access-prompt]").on('focus', function(e){
        var msg = '<span style="color: #2d6ca6">';
        msg += 'Скомбинируйте следующие цифры, чтобы дать пользователю необходимые права доступа:<br>';
        msg += '1 - права преподавателя;<br>';
        msg += '2 - права модератора начального уровня (добавл., редакт. групп, нагрузок);<br>';
        msg += '3 - права модератора продвинутого уровня (приглашение, удаление пользователей);<br>';
        msg += '4 - права администратора (удаление, редактирование нагрузок и журналов других пользователей);<br>';
        msg += '</span>';
        showMessage($(".message"), msg);
    })
    
    
    $('[model]').on('change', function(e){
        model[$(e.target).attr('model')] = e.target.value;
    });
    
    $("#inviteButton").on('click', function(e){
        if(!checkRequired($("[required]")))
            showMessage($(".message"), 'Не все поля заполнены!');
        else if(!checkLatin($("[latin]").val()))
            showMessage($(".message"), 'В ник-нейме допустимо использовать только латинские символы и цифры');
        else if(!checkLatin($("[numeric]").val()))
            showMessage($(".message"), 'Обратите внимание на правила ввода прав доступа');
        else {
            queryServer('/invite', ['INVITE', model], function(data){
                data = JSON.parse(data);
                if(data[0] === "OK")
                    nullModel(model);
                else if(data[0] === 'ERROR'){
                    if(data[1] === 'duplicate')
                        showMessage($(".message"), 'Пользователь с таким ник-неймом уже существует');
                    else showMessage($(".message"), 'Нам пришлось нейтрализировать ошибку, угрожавшую безопасности приложения, поэтому нам не удалось добавить пользователя в базу. Сожалеем :(');
                }
            });
        }
    });
}