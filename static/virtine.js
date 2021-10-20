$(function () {
    $('#reg_btn').click(function () {
        var vname = $("#vname").val();
        var vcode = $("#vcode").val();

        var fd = new FormData();
        fd.append("vname", vname);
        fd.append("vcode", vcode);

        $.ajax({
            type: 'POST',
            url: '/register',
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
    $('#exec_btn').click(function () {
        var args = $("#args").val();
        var vname = $("#vname").val();

        var fd = new FormData();
        fd.append("vname", vname);
        fd.append("args", args);

        $.ajax({
            type: 'POST',
            url: '/execute',
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
