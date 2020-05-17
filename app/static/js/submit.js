$(document).ready(function() {
    $("#submit").click(function() {
        var packet = {
            "title": $("#problemTitle").text(),
            "language": $("#language").val(),
            "code": editor.getValue()
        }
       var language = $("#language").val();
       $.ajax({
            url: '/judge',
            data: JSON.stringify(packet),
            type: 'POST',
            contentType: 'application/json',
            success: function(response) {
                if (response.hasOwnProperty('error')) {
                    alert(response['error']);
                }
                s = ""
                for (i in response) {
                    s+= "Test Case " + i + " " + response[i] + "\n";
                }
                alert(s);
            },
            error: function(response) { 
                alert("ERROR");
           }
       });
    });
});