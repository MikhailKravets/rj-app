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
            jContainer.css('display', 'block');
        }
        else {
            jContainer.html();
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
}
