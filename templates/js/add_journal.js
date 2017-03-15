function Controller(){
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
    
    var load_choice = [];
    var delay = 300;
    var t;
    var isWait = false;
    
    
    function updateModel(key, val){
        model[key] = val;
    }
    
    function checkList(list, value) {
        var new_list = [];
        for(var i = 0; i < list.length; i++){
            if(list[i].first.toLowerCase().search(value.toLowerCase()) !== -1)
                new_list.push(list[i]);
        }
        if(new_list.length == 0)
            return -1; // return list of indeces of right answers
        else return new_list;
    }
    
    function validateLoad(value){
        right = checkList(load_choice, value);
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
            console.log(load_choice);
            $(input).val(load_choice[i].first);
            input.focus();
            
            updateModel(key, input.val());
            updateChoiceView(container, [], true);
            
            setTimeout(function(){
                input.blur();
            }, 100);
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
                str += '<div class="secondComboHeader">'+ list[i].second +' семестр</div>';
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

                    right = checkList(load_choice, e.target.value);
                    console.log(right)
                    if (right === -1) {
                        console.log("Load from server");
                        queryServer('/journal/post', ["CHOICE", $(e.target).val()], function (data) {
                            data = JSON.parse(data);
                            load_choice = data[1];
                            updateChoiceView(container, load_choice, true);
                            isWait = false;
                        });
                    }
                    else{
                        updateChoiceView(container, right, true);
                        isWait = false;
                    }
                }, delay);
            }
            else {
                var container = $(e.target).closest(".inputTextShell").find(".comboContainer");
                load_choice = [];
                updateChoiceView(container, [], true);
            }
        }
    });
    $("[choice]").on('blur', function(e){
        setTimeout(function(){
            var archi = $(e.target).closest(".inputTextShell");
            if(!archi.find(".comboItem").is(":focus")){
                updateChoiceView(archi.find(".comboContainer"), [], false);
                if(!validateLoad(e.target.value))
                    $(e.target).addClass('unvalidated');
                else{
                    $(e.target).removeClass('unvalidated');
                    data = checkList(load_choice, e.target.value);
                    queryServer('/journal/post', ["STEP", data.first, data.secon, data.third], function (data) {
                        data = JSON.parse(data);
                        console.log(data);
                        $("#current").text(data[0]);
                        $("#max").text(data[1]);
                        $("#steps").css('visibility', 'visible');
                        $("#beforeView").css('display', 'none');
                        $("#stepView").html(data[2]);
                        regInputs($(".textField"));
                    });
                }
            }
        }, 30);
    });
    $("[choice]").on('keydown', function(e){
        var container = $(e.target).closest(".inputTextShell").find(".comboContainer");
        
        if(e.keyCode == 13){
            if(e.target.value !== ''){
                var key = $(e.target).attr('model');
                if (load_choice.length !== 0)
                    $(e.target).closest(".inputTextShell").find('.comboItem:first-child').click();
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
        
        if(load_choice.length !== 0)
            updateChoiceView(container, load_choice, true);
        else
            queryServer('/journal/post', ["CHOICE", $(e.target).val()], function (data){
                data = JSON.parse(data);
                load_choice = data[1];
                updateChoiceView(container, load_choice, true);
            });
    });
}