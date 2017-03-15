function Controller(){
    var model = {};
    
    $("[model]").on('change', function(e){
        var target = $(e.target);
        var mvalue = target.val(), defvalue = target.attr('default');
        var key = target.attr('model');
        if(key !== 'none'){
            if(mvalue === defvalue || (mvalue === "" && defvalue === undefined))
                delete model[key]
            else
                model[key] = mvalue;
        }
    });
    
    $("#saveButton").on('click', function(e){
        if(Object.keys(model).length !== 0){
            if(!checkRequired($("[required]")))
                showMessage($(".message"), 'Некоторые поля для ввода просто не могут быть пустыми. Например, ник-нейм, фамилия или имя');
            else if(!checkLatin($("[latin]").val()))
                showMessage($(".message"), 'В ник-нейме допустимо использовать только латинские символы и цифры');
            else if(!checkEmail($("[email]").val()))
                showMessage($(".message"), 'Неправильно введен почтовый адрес');
            else if(model['password'] !== undefined && !checkEqual($("[equal]")))
                showMessage($(".message"), 'Введенные пароли не совадают');
            else {
                hideMessage($(".message"));
                trimModel(model);
                queryServer('/settings', ["UPDATE", model], function(data){
                    data = JSON.parse(data);
                    console.log(data);
                    if(data[0] == 'OK'){
                        model = {}
                        $("[equal]").val('');
                        showMessage($(".message"), '<span style="color: #2DA655">Изменения сохранены</span>');
                    }
                    else if(data[0] == 'ERROR'){
                        if(data[1] == 'duplicate')
                            showMessage($(".message"), 'Пользователь с таким ник-неймом уже существует!');
                        else 
                            showMessage($(".message"), 'Нам пришлось нейтрализировать ошибку, угрожавшую безопасности приложения, поэтому нам не удалось сохранить изменения в базу. Сожалеем :(');
                    }
                });
            }
        }
    });
}