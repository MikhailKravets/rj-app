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
    showNavigation($("#navigationButton"), $("#navigation"));
}