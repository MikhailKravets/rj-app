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
    
    window.history.pushState('page2', 'title', url);
    setTimeout(function(){
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'html',
            data: 'inline=1'
        }).then(function(data){
            if(data == 'DENIED')
                window.location.reload();
            else{
                view.html(data);
                setTimeout(function(){
                    view.removeClass("view-faded");
                }, 100)
                controller = Controller;
                controller();
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
    console.log(window.location.pathname);
    app.get(window.location.pathname);
    
    showNavigation($("#navigationButton"), $("#navigation"));
    
    $("[profile]").on('click', function(e){
        app.get('/profile');
    });
    
    $("[invite]").on('click', function(e){
        app.get('/invite');
    });
}