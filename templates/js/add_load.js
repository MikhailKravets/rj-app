function Controller() {
    var model = {
        lecture: "0",
        practice: "0",
        labor: "0",
        seminar: "0",
        
        self_lecture: "0",
        self_practice: "0",
        self_labor: "0",
        self_seminar: "0"
    };
    
    var teach_choice = [];
    var disc_choice = [];
    var group_choice = [];

    var delay = 300;
    var t;
    var isWait = false;

    function updateModel(key, val){
        model[key] = val;
    }
    
    function intifyModel(){
        var keys = Object.keys(model);
        for(var i = 0; i < keys.length; i++){
            var n = parseInt(model[keys[i]]);
            if(!isNaN(n))
                model[keys[i]] = n;
        }
    }
    
    function checkList(list, value) {
        var new_list = [];
        for(var i = 0; i < list.length; i++){
            if(list[i].first.toLowerCase().search(value.toLowerCase()) !== -1)
                new_list.push(list[i]);
        }
        console.log(new_list);
        if(new_list.length == 0)
            return -1; // return list of values of right answers
        else return new_list;
    }
    
    function validateTeacher(value){
        right = checkList(teach_choice, value);
        return right !== -1
    }
    function validateDisc(value){
        right = checkList(disc_choice, value);
        return right !== -1
    }
    function validateGroup(value){
        right = checkList(group_choice, value);
        return right !== -1
    }
    
    function registerComboEvents(jContainer){
        var comboItem = jContainer.find(".comboItem");
        
        comboItem.on('click', function(e){
            var archi = $(e.target).closest(".inputTextShell");
            var container = archi.find(".comboContainer");
            var i = $(e.target).closest(".comboItem").index();
            var input = archi.find('input');
            var key = input.attr('model');
            
            if (key === 'teacher')
                $(input).val(teach_choice[i].first);
            else if (key === 'discipline')
                $(input).val(disc_choice[i].first);
            else if (key === 'group')
                $(input).val(group_choice[i].first);
            input.focus();
            
            updateModel(key, input.val());
            updateChoiceView(container, [], true);
        });
        comboItem .on('keydown', function(e){
            if(e.keyCode === 13)
                $(e.target).click();
            else if(e.keyCode === 38){
                e.preventDefault();
                if($(e.target).index() === 0){
                    $(e.target).closest(".inputTextShell").find('input').focus();
                }
                else
                    $(e.target).prev().focus();
            }
            else if(e.keyCode === 40){
                e.preventDefault();
                $(e.target).next().focus();
            }
        });
        comboItem.on('blur', function(e){
            setTimeout(function(){
                if(!comboItem.is(":focus") && !jContainer.closest(".inputTextShell").find('input').is(":focus"))
                    updateChoiceView(jContainer, [], true);
            }, 30);
        });
    }
    
    function updateChoiceView(jContainer, list, nullify=false){
        if(nullify)
            jContainer.html("");
        if(list.length !== 0){
            for(var i = 0; i < list.length; i++){
                var str = '<div class="comboItem" tabindex="1">';
                str += '<div class="firstComboHeader">' + list[i].first + '</div>';
                str += '<div class="secondComboHeader">'+ list[i].second +'</div>';
                str += '</div>';
                jContainer.html(jContainer.html() + str);
            }
            registerComboEvents(jContainer);
            jContainer.css('display', 'block');
        }
        else {
            jContainer.html("");
            jContainer.css('display', 'none');
        }
        //jContainer.closest(".inputTextShell").find('input').focus();
    }

    $("[choice]").on('input', function (e) {
        if (t) {
            clearTimeout(t);
            t = undefined;
        }
        if (!isWait) {
            var key = $(e.target).attr('model');
            if(e.target.value !== ""){
                t = setTimeout(function () {
                    isWait = true;
                    var right = -1;
                    var container = $(e.target).closest(".inputTextShell").find(".comboContainer");

                    if (key === 'teacher')
                        right = checkList(teach_choice, e.target.value);
                    else if (key === 'discipline')
                        right = checkList(disc_choice, e.target.value);
                    else if (key === 'group')
                        right = checkList(group_choice, e.target.value);
     
                    if (right === -1) {
                        console.log("Load from server");
                        queryServer('/load/post', ["CHOICE", key, $(e.target).val()], function (data) {
                            data = JSON.parse(data);

                            if (key === 'teacher'){
                                teach_choice = data[1];
                                updateChoiceView(container, teach_choice, true);
                            }
                            else if (key === 'discipline'){
                                disc_choice = data[1];
                                updateChoiceView(container, disc_choice, true);
                            }
                            else if (key === 'group'){
                                group_choice = data[1];
                                updateChoiceView(container, group_choice, true);
                            }
                        });
                    }
                    else{
                        updateChoiceView(container, right, true);
                    }
                    isWait = false;
                }, delay);
            }
            else {
                var container = $(e.target).closest(".inputTextShell").find(".comboContainer");
                if (key === 'teacher')
                    teach_choice = [];
                else if (key === 'discipline')
                    disc_choice = [];
                else if (key === 'group')
                    group_choice = [];
                updateChoiceView(container, [], true);
            }
        }
    });
    $("[choice]").on('blur', function(e){
        setTimeout(function(){
            var archi = $(e.target).closest(".inputTextShell");
            var key = $(e.target).attr('model');
            if(!archi.find(".comboItem").is(":focus")){
                updateChoiceView(archi.find(".comboContainer"), [], false);
                if (key === 'teacher'){
                    right = validateTeacher(e.target.value);
                }
                else if (key === 'discipline'){
                    right = validateDisc(e.target.value);
                }
                else if (key === 'group'){
                    right = validateGroup(e.target.value);
                }
                if(!right)
                    $(e.target).addClass('unvalidated');
                else $(e.target).removeClass('unvalidated');
            }
        }, 30);
    });
    $("[choice]").on('keydown', function(e){
        var container = $(e.target).closest(".inputTextShell").find(".comboContainer");
        
        if(e.keyCode == 13){
            if(e.target.value !== ''){
                var key = $(e.target).attr('model');

                if (key === 'teacher' && teach_choice.length !== 0)
                    $(e.target).val(teach_choice[0].first);
                else if (key === 'discipline' && disc_choice.length !== 0)
                    $(e.target).val(disc_choice[0].first);
                else if (key === 'group' && group_choice.length !== 0)
                    $(e.target).val(group_choice[0].first);
                
                updateModel(key, e.target.value);
                updateChoiceView(container, [], true);
            }
        }
        else if(e.keyCode === 40){
            container.find(".comboItem").first().focus();
        }
    });
    $(".comboTriangle").on('click', function(e){
        var input = $(e.target).closest(".inputTextShell").find("input");
        var container = $(e.target).closest(".inputTextShell").find(".comboContainer");
        var key = input.attr("model");
        
        if(key === 'teacher'){
            if(teach_choice.length !== 0)
                updateChoiceView(container, teach_choice, true);
            else
                queryServer('/load/post', ["CHOICE", key, $(e.target).val()], function (data){
                    data = JSON.parse(data);
                    
                    teach_choice = data[1];
                    updateChoiceView(container, teach_choice, true);
                });
                
        }
        else if(key === 'discipline'){
            if(disc_choice.length !== 0)
                updateChoiceView(container, disc_choice, true);
            else
                queryServer('/load/post', ["CHOICE", key, $(e.target).val()], function (data){
                    data = JSON.parse(data);
                    
                    disc_choice = data[1];
                    updateChoiceView(container, disc_choice, true);
                });
        }
        else if(key === 'group'){
            if(group_choice.length !== 0)
                updateChoiceView(container, group_choice, true);
            else
                queryServer('/load/post', ["CHOICE", key, $(e.target).val()], function (data){
                    data = JSON.parse(data);
                    
                    group_choice = data[1];
                    updateChoiceView(container, group_choice, true);
                });
        }
    });
    
    $('[model]').on('change', function(e){
        model[$(e.target).attr('model')] = e.target.value;
    });
    
    $("#addButton").on('click', function(e){
        if(!checkRequired($("[required]")))
            showMessage($(".message"), 'Не все поля заполнены!');
        else if(!checkNumeric($("[numeric]")))
            showMessage($(".message"), 'В некоторые поля можно ввести только числовые значения!');
        else{
            trimModel(model);
           // intifyModel(model);
            console.log(model);
            queryServer('/load/post', ['ADD', model], function(data){
                data = JSON.parse(data);
                console.log(data);
                if(data[0] === 'OK'){
                    showMessage($(".message"), '<span style="color: #2DA655">Нагрузка добавлена в базу</span>');
                    defaultify();
                    nullModel(model, true);
                }
                else if(data[0] === 'ERROR'){
                    if(data[1] === 'multiple')
                        showMessage($(".message"), 'У данного преподавателя в заданном семестре уже существет такая нагрузка!');
                    else
                        showMessage($(".message"), 'Нам пришлось нейтрализировать ошибку, угрожавшую безопасности приложения, поэтому нам не удалось сохранить изменения в базу. Сожалеем :(');
                }
            });
        }
    });
}
