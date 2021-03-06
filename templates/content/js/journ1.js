function StepController(max_hours, update){
    var model = {}
    var rem = JSON.parse(JSON.stringify(max_hours));
    initModel(model);
    
    function zerofy(m){
        var k = Object.keys(m);

        for(var i = 0; i < k.length; i++){
            if(m[k[i]] === "")
                m[k[i]] = '0';
        }
    }
    
    function calcRemain(attr_name){
        console.log(rem);
        var sums = {};
        var jElem = $('[' + attr_name + ']');
        var old = 0;
        
        jElem.on('focusin', function(e){
            var key = $(e.target).attr(attr_name);
            var sum = 0;
            var val = parseInt(e.traget);
            
            if(isNaN(val))
                old = 0;
            else old = val;
            
            var spec_elem = $('[' + attr_name + '=' + key + ']');
            
            for(var i = 0; i < spec_elem.length; i++){
                if(spec_elem[i].value !== '' && i !== spec_elem.index(e.target))
                    sum += parseInt(spec_elem[i].value);
            }
            sums[key] = sum;
        });
        jElem.on('input', function(e){
            var elem = $(e.target);
            var key = elem.attr(attr_name);
            var intval = parseInt(e.target.value);
            
            if(isNaN(intval)){
                elem.addClass('unvalidated');
            }
            else{
                elem.removeClass('unvalidated');
                rem[key] = max_hours[key] - sums[key] - intval + old;
                if(rem[key] < 0){
                    intval += rem[key];
                    e.target.value = intval;
                    rem[key] = 0;
                }
                $('[' + attr_name + '=' + key + ']').siblings('label').find('.rem-view').text(rem[key]);
            }
        });
    }
    
    calcRemain("remain");
    
    $('[model]').on('change', function(e){
        model[$(e.target).attr('model')] = e.target.value;
    });
        
    $("#m-amount").on('change', function(e){
        if(e.target.value === '1'){
            $("#m2Container").css('display', 'none');
            $("[requiredif]").attr('requiredif', 'false');
            $("[numericif]").attr('numericif', 'false');
        }
        else {
            $("#m2Container").css('display', 'block');
            $("[requiredif]").attr('requiredif', 'true');
            $("[numericif]").attr('numericif', 'true');
        }
    });
    
    $("#forwardButton").on('click', function(e){
        if(!checkRequired($("[required]")))
            showMessage($(".message"), 'Не все обязательные поля заполнены!');
        else if(!checkRequiredif($("[requiredif]")))
            showMessage($(".message"), 'Не все обязательные поля заполнены!');
        else if(!checkNumeric($("[numeric]")))
            showMessage($(".message"), 'В некоторые поля можно ввести только числовые значения!');
        else if(!checkNumericif($("[numericif]")))
            showMessage($(".message"), 'В некоторые поля можно ввести только числовые значения!');
        else {
            hideMessage($(".message"));
            trimModel(model);
            zerofy(model);
            
            console.log(model);
            
            queryServer('/journal/post', ["ADD", model], function (data){
                data = JSON.parse(data);
                update(data);
            });
        }
    });
}