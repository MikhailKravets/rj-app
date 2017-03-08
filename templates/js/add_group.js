function Controller(){
    var model = {};
    var students = [];
    var studentsView = $("[list-model]");
    
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
                    break;
                }
        }
        if(isNull){
            delete students.splice(index, 1);
            closest.remove();
        }
    });
}