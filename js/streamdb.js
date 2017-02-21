jQuery.getJSON("https://raw.githubusercontent.com/beardypig/tv-stream-db/master/docs/js/bootstrap.js" , function(data) {
    var tbl_body = "";
    var odd_even = false;
    jQuery.each(data, function() {
        var tbl_row = "";
        $.each(this, function(k , v) {
            tbl_row += "<td>"+v+"</td>";
        })
        tbl_body += "<tr class=\""+( odd_even ? "odd" : "even")+"\">"+tbl_row+"</tr>";
        odd_even = !odd_even;
    })
    jQuery("#streams tbody").html(tbl_body);
});