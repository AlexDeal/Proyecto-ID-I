jQuery(document).ready(function () {

  $("#submit-button").click(function (e) {
      e.preventDefault();
      $.ajax({
          type: "POST",
          url: "/chatbot",
          data: {
              question: $("#question").val()
          },
          success: function (result) {
              var chatBody = document.querySelector(".scroller");
              var divCpu = document.createElement("div");
              divCpu.className = "responseU visible";
              divCpu.innerHTML = "Abbott: " + result.response;
              var divUser = document.createElement("div");
              divUser.className = "response visible";
              divUser.innerHTML = $("#question").val();
              //$("#chatbody").append(divUser);
               chatBody.append(divUser);
              setTimeout(() => {
                  chatBody.append(divCpu);
                  //$("#chatbody").append(divCpu);
              }, 600);
              $("#question").val("")
          },
          error: function (result) {
              alert('error');
          }
      });
  });
});