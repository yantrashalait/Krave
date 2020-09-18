(function ($) {
  "use strict";
  $(document).ready(function () {
    function readURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
          $("#blah").attr("src", e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
      }
    }
    $("#imgInp").change(function () {
      readURL(this);
    });

    $(".fd-ct").select2({
      placeholder: "Select a Category",
    });

    $("#cl-bt").click(function (e) {
      e.preventDefault();
      var $self = $(this);
      var cloneIndex = $(".md-gp-ls").length;
      $self.before(
        $self
          .prev(".md-gp-ls")
          .clone()
          .attr("id", "md-gp-ls-id" + cloneIndex)
      );
    });

    $("#cl-bt-rd").click(function (e) {
      e.preventDefault();
      var $self = $(this);
      var cloneIndexrd = $(".md-gp-ls-rd").length;
      $self.before(
        $self
          .prev(".md-gp-ls-rd")
          .clone()
          .attr("id", "md-gp-ls-rd-id" + cloneIndexrd)
      );
    });

    $("#fd-it-ls-dt").DataTable();
  });

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
