(function () {

  "use strict";

  function dragover(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#drag-dest").addClass("hover");
  }

  function dragleave(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#drag-dest").removeClass("hover");
  }
  $("#drag-dest").on("dragleave", dragleave);

  function add(e, data) {
    $("#fileupload").fileupload("disable");
    $("#drag-dest").removeClass("hover");
    $("#drag-before").hide();
    $("#drag-after").show();
    data.submit();
  }

  function drop(e, data) {
    $("#drag-dest").hide();
    window.location = data.result;
  }

  $(function () {
    $("#fileupload").fileupload({
      dataType: "json",
      dropZone: $("#drag-dest"),
      dragover: dragover,
      add: add,
      done: drop
    });
  });

})();
