function bindCaptchaBtnClick() {
    // #选择id
    $("#captcha-btn").on('click', function (event) {
        var email = $("input[name='email']").val();
        var $this = $(this);
        if (!email) {
            alert("请先输入邮箱！");
            return;
        }
        // 通过js发送请求，ajax。Async JavaScript And XML(JSON)
        $.ajax({
            url: '/user/captcha',
            method: "POST",
            data: {
                "email": email
            },
            success: function (res) {
                if (res['code'] == 200) {
                    $this.off('click');
                    var countDown = 60;
                    var timer = setInterval(function () {
                        countDown -= 1;
                        if (countDown > 0) {
                            $this.text(countDown + "秒后重新发送！");
                        }
                        else {
                            $this.text("获取验证码");
                            bindCaptchaBtnClick();
                            clearInterval(timer);
                        }
                    }, 1000)
                    alert("验证码发送成功！");

                } else {
                    alert(res['message']);
                }
            }
        }
        )
    })
}
// 文档元素加载后执行
$(function () {
    bindCaptchaBtnClick();
})