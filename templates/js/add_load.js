function Controller(){
    var teach_choice = [];
    var disc_choice = [];
    var group_choice = [];
    
    var delay = 400;
    var t;
    var isWait = false;
    
    function checkList(list){
        return -1; // return list of indeces of right answers
    }
    
    $("[choice]").on('input', function(e){
        if(t){
            clearTimeout(t);
            t = undefined;
        }
        if(!isWait){
            if(e.taret.value !== ''){
                t = setTimeout(function(){
                    isWait = true;
                    var key = $(e.target).attr('model');
                    var right = -1;
                    if(key === 'teacher')
                        right = checkList(teach_choice);
                    else if(key === 'discipline')
                        right = checkList(disc_choice);
                    else if(key === 'group')
                        right = checkList(group_choice);
                    if(right === -1){
                        queryServer('/load/post', ["CHOICE", key, $(e.target).val()], function(data){
                            data = JSON.parse(data);
                            console.log(data);
                        });
                    }
                    isWait = false;
                }, delay);
            }
        }
    });
}