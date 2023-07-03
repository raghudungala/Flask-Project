$(document).ready(function() {

  function toggle_display() {
    var content_section = $(".content_section")
    if (content_section.not(":visible")) {
        var skill_list = document.getElementById("skill_list");
        var value = skill_list.options[skill_list.selectedIndex].value
        document.getElementById("sid").value = value
        content_section.show();
    } else{
      content_section.hide()
    }
  }
  
  $("#questions").click(function() {
    $.ajax({
      type: "GET",
      url: $(this).attr("action"),
      data: $("#filter").serialize(), // serializes the form's elements.
      success: function(data) {
        $(".get_section").show().html(data)
      },
      error: function(error) {
        $(".get_section").show().html(error);
      }
    })  
  })

  $(".create").click(function() {
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $("#addquestion").serialize(), // serializes the form's elements.
      success: function(data) {
        $("button.close").trigger("click");
        flashMessage(data);
        // var question = data.question
        // var tr = "<tr id="+ question.id +"> <td>"+ question.tag +"</td> <td>"+ question.description +"</td> <td>"+ question.weightage +"</td>  <td>"+ question.user_id +"</td>  <td>"+ question.qtype_id +"</td>  <td>"+ question.sid +"</td> <td><button class='btn btn-warning' data-toggle='modal' target='#editQuestion'>Update</button></td>  <td><button class='btn btn-danger delete' action='delete/'+"+ question.id +" class='delete' data-confirm='Are you sure you want to delete?'>Delete</button></td> </tr>"
        // $("table tbody").append(tr);
      },
      error: function(error) {
        $(".get_section").show().html(error);
      }
    })
  })

  function flashMessage(data) {
    $("#flashmessage").html('<div class="alert alert-'+(data.hasOwnProperty("success") ? "success" : "danger")+' alert-dismissible fade show">'+ data.message +'<button type="button" class="close" data-dismiss="alert">&times;</button>  </div>');
  }

  $(".createuser").click(function() {
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $("#newuser").serialize(), // serializes the form's elements.
      success: function(data) {
        $("button.close").trigger("click");
        flashMessage(data);
        // var question = data.question
        // var tr = "<tr id="+ question.id +"> <td>"+ question.tag +"</td> <td>"+ question.description +"</td> <td>"+ question.weightage +"</td>  <td>"+ question.user_id +"</td>  <td>"+ question.qtype_id +"</td>  <td>"+ question.sid +"</td> <td><button class='btn btn-warning' data-toggle='modal' target='#editQuestion'>Update</button></td>  <td><button class='btn btn-danger delete' action='delete/'+"+ question.id +" class='delete' data-confirm='Are you sure you want to delete?'>Delete</button></td> </tr>"
        // $("table tbody").append(tr);
        setTimeout(function(){window.location.reload(); }, 300); 

      },
      error: function(error) {
        $(".get_section").show().html(error);
      }
    })
  })

  function flashMessage(data) {
    $("#flashmessage").html('<div class="alert alert-'+(data.hasOwnProperty("success") ? "success" : "danger")+' alert-dismissible fade show">'+ data.message +'<button type="button" class="close" data-dismiss="alert">&times;</button>  </div>');
  }
})



$(document).on("click", ".modalpopup, .editQuestion", function () {
    var id = $(this).attr("href");
    $.ajax({
      type: "GET",
      url: $(this).attr("action"),
      data: {"form_type": id},
      success: function(data) {
        $(id+" .modal-body").html(data);
        var c_list = $("#form select#c_list")
        $(c_list).val($(c_list).attr("cat-id"));

        var s_list = $("#form select#s_list")
        $(s_list).val($(s_list).attr("s-id"));

        var weightage = $("#form select#weightage")
        $(weightage).val($(weightage).attr("weightage"));

        var qtype = $("#form select#qtype_list");
        $(qtype).val($(qtype).attr("qtype-id"));

        if(id=="#exampleModal") {
          $("#form input").attr("readonly", true)
          $("#form select").attr("disabled", true)
        } else {
          $("#form input").attr("readonly", false)
          $("#form select").attr("disabled", false)
        }
      },
      error: function(error) {
        // $(".get_section").show().html(error);
      }
    })
  // $.each($(dis).data(), function(key,value) { $("td#"+key).text( $(dis).attr("data-"+key) ); })
});

