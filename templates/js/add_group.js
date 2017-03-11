function Controller(){    
    var model = {
        name: '',
        specialty: '',
        finance_form: '',
        study_form: '',
        university: '',
        qualification: ''
    };
    var students = [];
    var studentsView = $("[list-model]");
    
    
    function nullifyStudents(){
        students = [];
        var list_model = $("[list-model]");
        var first_copy = list_model.find('tr').first().clone(true);
        
        var model_keys = first_copy.find('[model-key]');
        for(var i = 0; i < model_keys.length; i++){
            if($(model_keys[i]).attr('novalidate') === undefined)
                $(model_keys[i]).val("");
        }
        
        list_model.html("")
        list_model.append(first_copy);
    }
    
    nullModel(model, true);
    
    studentsView.find('[model-key]').on('change', function(e){
        var closest = $(e.target).closest('tr');
        var length = closest.length;
        var index = closest.index();
        var finded = closest.find('[model-key]');

        
        if(index >= students.length){
            var obj = {};
            for(var i = 0; i < finded.length; i++)
                obj[$(finded[i]).attr('model-key')] = $(finded[i]).val();
            students.push(obj);
            
            var clone = closest.clone(true);
            var nullifyView = clone.find('[model-key]')
            for(var i = 0; i < nullifyView.length; i++){
                if($(nullifyView[i]).attr('novalidate') === undefined)
                    $(nullifyView[i]).val("")
            }
            closest.closest("tbody").append(clone);
        }
        else students[index][$(e.target).attr('model-key')] = $(e.target).val();
        
        var keys = Object.keys(students[index]);
        var isNull = true;
        for(var i = 0; i < keys.length; i++){
            if($(finded[i]).attr('novalidate') === undefined)
                if(students[index][keys[i]] !== ""){
                    isNull = false;
                    students[index][keys[i]]
                    break;
                }
        }
        if(isNull){
            delete students.splice(index, 1);
            closest.remove();
        }
    });
    
    $('[model]').on('change', function(e){
        model[$(e.target).attr('model')] = e.target.value;
    });
    
    $("#addButton").on('click', function(e){
        if(!checkRequired($("[required]")))
            showMessage($(".message"), 'Не все поля заполнены!');
        else if(students.length === 0)
            showMessage($(".message"), 'Добавьте студентов в группу!');
        else{
            hideMessage($(".message"));
            trimModel(model);
            for(var i = 0; i < students.length; i++)
                trimModel(students[i]);
            model.students = students;
            queryServer('/group/post', ['ADD', model], function(data){
                data = JSON.parse(data)
                console.log(data);
                
                if(data[0] === 'OK'){
                    showMessage($(".message"), '<span style="color: #2DA655">Группа добавлена в базу</span>');
                    defaultify();
                    nullModel(model, true);
                    nullifyStudents();
                }
                else if(data[0] === 'ERROR'){
                    if(data[1] === 'duplicity')
                        showMessage($(".message"), 'Группа с таким названием уже существует!');
                    else
                        showMessage($(".message"), 'Нам пришлось нейтрализировать ошибку, угрожавшую безопасности приложения, поэтому нам не удалось сохранить изменения в базу. Сожалеем :(');
                }
            })
        }
    });
}