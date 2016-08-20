function reply_zan(sig, reply_id, id_num) {
    id_num = id_num.toString();
    zans = $('#text_zan').val();
    var AjaxUrl = "/" + sig + "/reply/zan/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        if (Json.text_zan == 0) {
        }
        else {
            $("#text_zan_" + id_num).html(Json.text_zan);
        }
    });
}

function reply_del(sig, reply_id, id_num) {
    id_num = id_num.toString();
    var AjaxUrl = "/" + sig + "/reply/delete/" + reply_id;
    $.getJSON(AjaxUrl, function (Json) {
        if (Json.del_zan == 1)
        {
        $("#del_zan_" + id_num).html('');
            }
        else
        {
            alert('删除失败！');
        }
    });
}


function reply_it(sig, view_id) {
    var txt = $("#cnt_md").val();
    if (txt.length < 10) {
        return;
    }
    $.post("/" + sig + "/reply/add/" + view_id, {cnt_md: txt}, function (result) {
        var msg_json = $.parseJSON(result);
        $("#pinglun").load('/reply/get/' + msg_json.pinglun);
    });
    $('#cnt_md').val('');
    $('#cnt_md').attr("disabled", true);
    $('#btn_submit_reply').attr('disabled', true);
}
