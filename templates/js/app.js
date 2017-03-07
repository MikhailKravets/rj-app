function regInputs(jInput){
    jInput.on('input', function(e){
        if(e.target.value === ""){
            console.log('fdsfsdfds0');
            if($(e.target).next().hasClass('promptExpanded'))
                $(e.target).next().removeClass('promptExpanded');
        }
        else{
            if(!$(e.target).next().hasClass('promptExpanded'))
                $(e.target).next().addClass('promptExpanded');
        }
    });
}

function initModel(model){
    var melem = $("[model]");
    for(var i = 0; i < melem.length; i++)
        model[$(melem[i]).attr('model')] = melem[i].value;
}
function nullModel(model){
    $("[model]").val('');
    initModel(model);
}

function showMessage(jElem, msg){
    jElem.html(msg);
    jElem.css('display', 'block');
}
function hideMessage(jElem){
    jElem.css('display', 'none');
}

function checkRequired(jElem){
    for(var i = 0; i < jElem.length; i++)
        if(jElem[i].value === '')
            return false;
    return true;
}
function checkLatin(str){
    pattern = /[^A-Za-z0-9]+/i;
    if(pattern.test(str))
        return false;
    else return true;
}
function checkNumeric(str){
    pattern = /[^0-9]+/i;
    if(pattern.test(str))
        return false;
    else return true;
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
}