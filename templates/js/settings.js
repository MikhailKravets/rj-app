function Controller(){
    var model = {};
    
    $("[model]").on('change', function(e){
        var target = $(e.target);
        var mvalue = target.val(), defvalue = target.attr('default');
        var key = target.attr('model');
        if(mvalue === defvalue || (mvalue === "" && defvalue === undefined))
            delete model[key]
        else
            model[key] = mvalue;
    });
    
    $("#saveButton").on('click', function(e){
        
    });
}