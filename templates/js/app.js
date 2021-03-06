function regInputs(jInput){
    jInput.each(function(){
        if(this.value === "")
            $(this).next().removeClass('promptExpanded');
        else
            $(this).next().addClass('promptExpanded');
    });
    jInput.on('input blur', function(e){
        if(e.target.value === ""){
            if($(e.target).next().hasClass('promptExpanded'))
                $(e.target).next().removeClass('promptExpanded');
        }
        else{
            if(!$(e.target).next().hasClass('promptExpanded'))
                $(e.target).next().addClass('promptExpanded');
        }
    });
}

function trimModel(obj){
    var keys = Object.keys(obj);
    for(var i = 0; i < keys.length; i++)
        obj[keys[i]] = obj[keys[i]].trim();
}
function initModel(model){
    var melem = $("[model]");
    for(var i = 0; i < melem.length; i++)
        model[$(melem[i]).attr('model')] = melem[i].value;
}
function nullModel(model, init=true){
    var target = $("[model]");
    for(var i = 0; i < target.length; i++){
        var def = $(target[i]).attr('default');
        if(def !== undefined)
            $(target[i]).val(def)
        else $(target[i]).val('');
    }
    if(init)
        initModel(model);
}
function defaultify(){
    var target = $("[model]");
    for(var i = 0; i < target.length; i++){
        var def = $(target[i]).attr('default');
        if(def !== undefined)
            $(target[i]).val($(target[i]).attr('default'));
        else $(target[i]).val('');
    }
}

function showMessage(jElem, msg){
    jElem.html(msg);
    jElem.css('display', 'block');
}
function hideMessage(jElem){
    jElem.css('display', 'none');
}

function checkRequired(jElem){
    for(var i = 0; i < jElem.length; i++){
        if(jElem[i].value === ''){
            $(jElem[i]).addClass('unvalidated');
            return false;
        }
        else $(jElem[i]).removeClass('unvalidated');
    }
    return true;
}
function checkRequiredif(jElem){
        for(var i = 0; i < jElem.length; i++){
        if(jElem[i].value === '' && jElem.attr('requiredif') === 'true'){
            $(jElem[i]).addClass('unvalidated');
            return false;
        }
        else $(jElem[i]).removeClass('unvalidated');
    }
    return true;
}
function checkLatin(str){
    var pattern = /[^A-Za-z0-9]+/i;
    if(pattern.test(str))
        return false;
    else return true;
}
function checkEmail(str){
    var pattern = /[A-Za-z0-9]+@{1}[A-Za-z0-9]+\.[A-Za-z0-9]+/i;
    return pattern.test(str);
}
function checkNumeric(jElem){
    pattern = /[^0-9]+/i;
    for(var i = 0; i < jElem.length; i++){
        if(pattern.test(jElem[i].value)){
            $(jElem[i]).addClass('unvalidated');
            return false;
        }
        else $(jElem[i]).removeClass('unvalidated');
    }
    return true;
}
function checkNumericif(jElem){
    pattern = /[^0-9]+/i;
    for(var i = 0; i < jElem.length; i++){
        if(pattern.test(jElem[i].value) && jElem.attr('numericif') == 'true'){
            $(jElem[i]).addClass('unvalidated');
            return false;
        }
        else $(jElem[i]).removeClass('unvalidated');
    }
    return true;
}
function checkEqual(jElem){
    var val = jElem[0].value;
    for(var i = 1; i < jElem.length; i++)
        if(jElem[i].value !== val)
            return false;
    return true;
}

function queryServer(url, obj, callback){
    $.ajax({
        url: url,
        method: 'POST',
        data: JSON.stringify(obj)
    }).then(function(data){
        if(data === 'DENIED')
            window.location.reload();
        else if(data === '405')
            window.location.assign('/profile');
        else callback(data);
    });
}

function quit(){
    $.ajax({
        url: '/',
        method: 'POST',
        data: JSON.stringify(['QUIT'])
    }).then(function(data){
        console.log(data);
        if(data === 'OK')
            window.location.assign('/auth');
    });
}

function Application(jView){
    this.view = jView;
    this.controller = '';
}
Application.prototype.get = function(url){
    var view = this.view;
    var controller = this.controller;
    view.addClass('view-faded');
    
    if(url === '/')
        url = '/profile';
    
    // TODO: register events of back/forward browser buttons
    window.history.pushState('page2', 'title', url);
    setTimeout(function(){
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'html',
            data: 'inline=1'
        }).then(function(data){
            if(data === 'DENIED')
                window.location.reload();
            else if(data === '405')
                window.location.assign('/profile');
            else{
                view.html(data);
                setTimeout(function(){
                    view.removeClass("view-faded");
                }, 100)
                controller = Controller;
                controller();
                regInputs($('input'));
            }
        });
    }, 20);
}


function showNavigation(menuButtonElem, navigationElem){
    menuButtonElem.on('click', function(e){
        if(navigationElem.hasClass("navigationHidden")) {
            navigationElem.removeClass("navigationHidden");
            navigationElem.addClass("navigationExpanded");
            menuButtonElem.removeClass("navigationButtonHidden");
        }
        else {
//            angular.element("#moreIconsContainer").css("display", "none");
//            angular.element("#showMoreIcons").removeClass("iconButtonExpanded");
            
            navigationElem.removeClass("navigationExpanded");
            navigationElem.addClass("navigationHidden");
            menuButtonElem.addClass("navigationButtonHidden");
        }
    });
}


window.onload = function(){
    var app = new Application($("#view"));
    app.get(window.location.pathname);
    showNavigation($("#navigationButton"), $("#navigation"));
    
    $("[quit]").on('click', function(e){
        quit();
    });
    
    $("[profile]").on('click', function(e){
        app.get('/profile');
    });
    
    $("[invite]").on('click', function(e){
        app.get('/invite');
    });
    
    $("[addDiscipline]").on('click', function(e){
        app.get('/discipline/add');
    });
    
    $("[addgroup]").on('click', function(e){
        app.get('/group/add');
    });
    
    $("[addload]").on('click', function(e){
        app.get('/load/add');
    });
    
    $("[settings]").on('click', function(e){
        app.get('/settings');
    });
    
    $("[addjournal]").on('click', function(e){
        app.get('/journal/add');
    });
}