function Application(jView){
    this.view = jView;
    this.controller = '';
}
Application.prototype.get = function(url){
    $.ajax({
        url: url,
        method: 'GET',
        data: 'inline=1'
    }).then(function(data){
        this.view.html(data);
        this.controller = controller;
    });
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
    showNavigation($("#navigationButton"), $("#navigation"));
    
    $("[profile]").on('click', function(e){
        app.get('/profile');
    });
}