$('.switch').on('click',function(){
    $('.register-window').toggleClass('hidden')
    $('.login-window').toggleClass('hidden')
})
$('.register-window input[name="username"]').addClass('col-12 size-one')
$('.register-window input[name="username"]').css('padding','10px')
$('.register-window input[name="email"]').addClass('col-12 size-one')
$('.register-window input[name="email"]').css('padding','10px')
$('.register-window input[name="password"]').addClass('col-12 size-one')
$('.register-window input[name="password"]').css('padding','10px')
$('.errorlist').addClass('d-flex col-12 px-0 left-ul')
$('.errorlist').css('color','rgb(255,0,0)')