function Controller(){
    var model = {
        name: '',
        feature: '',
        cycle: '',
        code: ''
    }
    
    $('[model]').on('change', function(e){
        model[$(e.target).attr('model')] = e.target.value;
    });
    
    $("#addButton").on('click', function(e){
        if(!checkRequired($("[required]")))
            showMessage($(".message"), 'Не все поля заполнены!');
        else{
            hideMessage($(".message"));
            trimModel(model);
            queryServer('/discipline/post', ["ADD", model], function(data){
                data = JSON.parse(data);
                if(data[0] === 'OK'){
                    showMessage($(".message"), '<span style="color: #2DA655">Дисциплина добавлена в базу</span>');
                    defaultify();
                    nullModel(model, true);
                }
                else if(data[0] === 'ERROR'){
                    if(data[1] === 'duplicity')
                        showMessage($(".message"), 'Группа с таким названием уже существует!');
                    else
                        showMessage($(".message"), 'Нам пришлось нейтрализировать ошибку, угрожавшую безопасности приложения, поэтому нам не удалось сохранить изменения в базу. Сожалеем :(');
                }
            });
        }
    });
}