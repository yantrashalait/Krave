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

    function readImageURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $('#image_blah').attr('src', e.target.result);
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

    function readCatURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $('#cat_image_blah').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
      }
    }

    function readRestaurantLogoURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $('#rest_blah').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
      }
    }

    function readRestaurantImgURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $('#rest_img_blah').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
      }
    }

    $("#id_logo").change(function() {
      readURL(this);
    });

    $("#imgInp").change(function() {
      readFoodURL(this);
    });

    $('#id_img').change(function(){
      readFoodURL(this);
    });

    $("#id_image").change(function(){
      readImageURL(this);
    });

    $("#id_cat_image").change(function(){
      readCatURL(this);
    });

    $("#restImgInp").change(function() {
      readRestaurantImgURL(this);
    });

    $("#restInp").change(function() {
      readRestaurantLogoURL(this);
    });

    $('.fd-ct').select2({
        placeholder: "Select a Category"
    });

    $('#food-select').select2({
      placeholder: "Select Food"
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

    //checkbox
    $("#demo").easySelect({
        showEachItem: true,
        dropdownMaxHeight: "100px",
    });

    //cuisines selection
    $("#cus_itm").easySelect({
        search: true,
        showEachItem: true,
        placeholder: "Select cuisines type",
        dropdownMaxHeight: "auto",
    });
    //date filter
    $("#kronos9-1").kronos({
        periodTo: "#kronos9-2",
        initDate: "mmddyy",
    });
    $("#kronos9-2").kronos({
        periodFrom: "#kronos9-1",
        initDate: "mmddyy",
    });

})(window.jQuery);
