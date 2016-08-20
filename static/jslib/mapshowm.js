
$(document).ready(function () {

$('#act_collect').click(function () {
$.ajax({
url: "/collect/" + post_uid,
type: 'GET',
cache: false,
data: {},
dataType: 'html',
timeout: 1000,
error: function () {
alert('请登陆后进行收藏！')
},
success: function (result) {
$('#text_collect').text('成功收藏');
$('#text_collect').css('color', 'red');
}
});
});

});