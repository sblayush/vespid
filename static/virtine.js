$(function () {
    $('#create_btn').click(function () {
        var vname = $("#vname").val();
        var vcode = $("#vcode").val();

        var fd = new FormData();
        fd.append("vname", vname);
        fd.append("vcode", vcode);

        $.ajax({
            type: 'POST',
            url: '/actions/create',
            data: fd,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                alert(data);
                res = JSON.parse(data)
            },
        });
    });
});

$(function () {
    $('#invoke_btn').click(function () {
        var args = $("#args").val();
        var vname = $("#vname").val();

        var fd = new FormData();
        fd.append("vname", vname);
        fd.append("args", args);

        $.ajax({
            type: 'POST',
            url: '/actions/invoke',
            data: fd,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
                alert(data);
                res = JSON.parse(data)
            },
        });
    });
});
