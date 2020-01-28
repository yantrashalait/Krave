(function($) {
'use strict'; 
$(document).ready(function(){
    $('.success__strories__carousel').owlCarousel({
            loop: true,
            rewind: true,
            responsiveClass: true,
            nav: true,
            smartSpeed: 500,
            dots: false,
            navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:1
                },
                1000:{
                    items:1
                }
            }
        });

    $('.category_nav_caro').owlCarousel({
        autoWidth:true,
        loop: false,
        rewind: true,
        responsiveClass: true,
        nav: true,
        margin: 30,
        smartSpeed: 500,
        dots: false,
        nav: false
})


    // $("#more__info").click(function(){
    //     $("#more__inf__hldr").css({'display': 'flex', 'position' : 'fixed'});
    // });

    $(".map__close__btn").click(function(){
        $("#more__inf__hldr").css({'display': 'none'});
    });



    // $("#food__detail").click(function(){
    //     $("#food__decspt__handler").css({'display': 'flex', 'position': 'fixed' });
    // });
    $(".popups__close__button").click(function(){
        $("#food__decspt__handler").css({'display': 'none'});
    });

   $("#cart_drpdwn").click(function(){
        $(".order__detail").css({'right' : '0'})
   });
   $('.order__close__btn').click(function(){
        $(".order__detail").css({'right' : '-100%'})
   })

   $(".drpdwn_cls").click(function(){
    $("#cart__popup").css({'display' : 'none'})
   })

   $("#notify_drpdwn").click(function(){
        $("#nav__popup").css({'display' : 'block'})
   });

   $(".drpdwn_cls").click(function(){
    $("#nav__popup").css({'display' : 'none'})
   })



// for food item increment and drecement
$(function() {
  $('.minus,.add').on('click', function() {
    var $qty = $(this).closest('p').find('.qty'),
      currentVal = parseInt($qty.val()),
      isAdd = $(this).hasClass('add');
    !isNaN(currentVal) && $qty.val(
      isAdd ? ++currentVal : (currentVal > 0 ? --currentVal : currentVal)
    );
  });
});


// for responsive menu

$('.resp__menu__icn').click(function(){
  $('.top__navbar').toggle();
  $('body').css({'overflow' : 'hidden'});
})

$('.close__resp__menu').click(function(){
  $('.top__navbar').hide();
  $('body').css({'overflow' : 'inherit'});
})



$('.category_nav_caro .owl-item').click(function(e){
  e.preventDefault();
  $(this).addClass('active-second');
   $(this).siblings().removeClass('active-second');
  
})

$("#user__pofl_drpdown").click(function(){
  $("#user__detail__drp").css({'display' : 'block'})
});
$(".drpdwn_cls").click(function(){
$("#user__detail__drp").css({'display' : 'none'})
})

});// document ready

$("#place_order").click(function(){
  $("#order__place").css({'display' : 'block'})
});

$(".pop__up__order__placed___close").click(function(){
 $("#order__place").css({'display' : 'none'})
})

})(window.jQuery);  