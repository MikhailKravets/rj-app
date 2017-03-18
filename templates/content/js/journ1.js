function StepController(){
    var model = {}
    
    initModel(model);
    
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
        console.log(model);
        if(!checkRequired($("[required]")))
            showMessage($(".message"), 'Не все обязательные поля заполнены!');
        else if(!checkRequiredif($("[requiredif]")))
            showMessage($(".message"), 'Не все обязательные поля заполнены!');
        else if(!checkNumeric($("[numeric]")))
            showMessage($(".message"), 'В некоторые поля можно ввести только числовые значения!');
        else if(!checkNumericif($("[numericif]")))
            showMessage($(".message"), 'В некоторые поля можно ввести только числовые значения!');
        else console.log("tadammm");
    });
}