$(function () {
    $('#create_btn').click(function () {
        var vname = $("#vname").val();
        var vcode = $("#vcode").val();

        var sendInfo = {
            "vname": vname,
            "vcode": vcode,
            "language": "c"
        }

        $.ajax({
            type: 'POST',
            url: '/actions/'+vname+'/create',
            data: JSON.stringify(sendInfo),
            contentType: "application/json; charset=utf-8",
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                alert(data.resp);
                res = data
            },
            error: function (data) {
                console.log(data);
                alert(data.responseJSON.resp);
                res = data
            },
        });
    });
});

$(function () {
    $('#invoke_btn').click(function () {
        var args = $("#args").val();
        var vname = $("#vname").val();

        var sendInfo = {
            "vname": vname,
            "vargs": args
        }

        $.ajax({
            type: 'POST',
            url: '/actions/'+vname+'/invoke',
            data: JSON.stringify(sendInfo),
            contentType: "application/json; charset=utf-8",
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                alert(data.resp);
                res = data
            },
            error: function (data) {
                console.log(data);
                alert(data.responseJSON.resp);
                res = data
            },
        });
    });
});
