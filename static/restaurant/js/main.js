(function($) {
'use strict';
$(document).ready(function(){

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#blah').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]);
  }
}

function readFoodURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#food_blah').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]);
  }
}

$("#id_logo").change(function() {
  readURL(this);
});

$('#id_img').change(function(){
  readFoodURL(this);
})

$('.fd-ct').select2({
    placeholder: "Select a Category"
});



$("#cl-bt").click(function (e) {
    e.preventDefault();
    var $self = $(this);
    var cloneIndex = $(".md-gp-ls").length;
    $self.before($self.prev('.md-gp-ls').clone().attr("id", "md-gp-ls-id" +  cloneIndex));
});


// $("#cl-bt-rd").click(function (e) {
//     e.preventDefault();
//     var $self = $(this);
//     var cloneIndexrd = $(".md-gp-ls-rd").length;
//     $self.before($self.prev('.md-gp-ls-rd').clone().attr("id", "md-gp-ls-rd-id" +  cloneIndexrd));
// });


$('#fd-it-ls-dt').DataTable();

});// document ready


})(window.jQuery);
