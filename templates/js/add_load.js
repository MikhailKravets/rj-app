function Controller() {
    var model = {};
    
    var teach_choice = [];
    var disc_choice = [];
    var group_choice = [];

    var delay = 300;
    var t;
    var isWait = false;

    function checkList(list, value) {
        var new_list = [];
        for(var i = 0; i < list.length; i++){
            if(list[i].first.toLowerCase().search(value) !== -1)
                new_list.push(list[i]);
        }
        if(new_list.length == 0)
            return -1; // return list of indeces of right answers
        else return new_list;
    }
    
    function registerComboEvents(jContainer){
        jContainer.find(".comboItem").on('click', function(e){
            var archi = $(e.target).closest(".inputTextShell");
            var container = archi.find(".comboContainer");
            var i = $(e.target).index();
            var input = archi.find('input');
            var key = input.attr('model');
            console.log(key);
            if (key === 'teacher')
                $(input).val(teach_choice[i].first);
            else if (key === 'discipline')
                $(input).val(disc_choice[i].first);
            else if (key === 'group')
                $(input).val(group_choice[i].first);
            input.focus();
            updateChoiceView(container, [], true);
        });
        var comboItem = jContainer.find(".comboItem");
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
    }

    $("[choice]").on('input', function (e) {
        if (t) {
            clearTimeout(t);
            t = undefined;
        }
        if (!isWait) {
            var key = $(e.target).attr('model');
            if(e.target.value){
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
            if(!archi.find(".comboItem").is(":focus"))
                updateChoiceView(archi.find(".comboContainer"), [], true);
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
                updateChoiceView(container, [], true);
            }
        }
        else if(e.keyCode === 40){
            container.find(".comboItem").first().focus();
        }
    });
    
    // TODO: handle svg triangle button
}
