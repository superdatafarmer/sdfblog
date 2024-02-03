// 点击显示子菜单
$(".ws-header-more").on("click", function () {
    $("body").addClass("ws-nav-show ws-shade-show");
});
$(".ws-menu-bar").on("click", function () {
    $("body").addClass("ws-menu-show ws-shade-show");
});
$(".layui-fixbar #toc-icon").on("click", function () {
    $("body").addClass("ws-side-show ws-shade-show");
});
$(".ws-shade").on("click", function () {
    $("body").removeClass("ws-nav-show ws-menu-show ws-side-show ws-shade-show");
});

//回到顶部
$(window).scroll(function () {
    const toTop = $('.layui-fixbar #top-icon');
    toTop.hide();
    if ($(window).scrollTop() >= 70) {
        toTop.show();
    }
});
$(".layui-fixbar #top-icon").click(function () {
    const speed = 400; //滑动的速度
    $('body,html').animate({
        scrollTop: 0
    }, speed);
    return false;
});

$(document).ready(function () {
    // 渲染前修改html，主要是调整code适配layui
    // 多段代码要遍历
    $(".ws-content .ws-center-detail .codehilite").each(function (index,element){
        var code = $(this).children("code").text();  // 获取标签内文本
        var lang = $(this).children("code").attr("class");
        // 因为不好处理语言，所以先将语言加进属性
        if(lang != undefined && lang != ""){
           lang = lang.split("-")[1];
           $(this).attr("lay-options","{lang: '" + lang + "'}");
        }
        // 因为html会被渲染，所以先转成实体字符
        if(lang = 'html'){
            code = code.replaceAll('>','&gt;').replaceAll('<','&lt;');
        }
        $(this).children("code").remove();  // 删除标签
        $(this).append(code);  // 标签内新增文本
    });
    // 引用样式设置
    $(".ws-content .ws-center-detail blockquote").each(function (index,element){
       $(this).addClass("layui-elem-quote");
    });
    // 引用样式设置
    $(".ws-content .ws-center-detail table").each(function (index,element){
       $(this).addClass("layui-table");
    });
    // 生成toc
    $(".ws-content .ws-center-detail h1,.ws-content .ws-center-detail h2,.ws-content .ws-center-detail h3").each(function (index,element){
       var tag = $(this).prop("tagName");
       var text = $(this).text();
       var id = $(this).attr("id")
       if(tag == "H1"){
           var html = '<li class=""><a href="#' + id + '" title = "' + text + '">' + text + '</a></li>';
           $(".ws-side ul").append(html);
           $(this).attr("lay-toc","{}");
       }else if(tag == "H2"){
           var html = '<li level="2"><a href="#' + id + '" title = "' + text + '">' + text + '</a></li>';
           $(".ws-side ul").append(html);
           $(this).attr("lay-toc","{level: 2}");
       }else{
           var html = '<li level="3"><a href="#' + id + '" title = "' + text + '">' + text + '</a></li>';
           $(".ws-side ul").append(html);
           $(this).attr("lay-toc","{level: 3}");
       }
    });
    //锚点平滑移动到指定位置
    $('.ws-content .ws-side .ws-dir-ul li a').click(function () {
        const href = $(this).attr('href');
        console.log('---->')
        console.log($($.attr(this, 'href')).offset().top);
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top - 70
        }, 200);
        history.pushState(null, null, href); // 更新URL，显示 #
        $("body").removeClass("ws-side-show ws-shade-show");
    });
    $(window).scroll(function () {
        const scrollPos = $(document).scrollTop();
        // 遍历每个导航链接
        $('.ws-content .ws-side .ws-dir-ul li').each(function () {
            // 获取当前元素的子元素的第一个元素
            const target = $(this).children().first().attr('href');
            // 检查滚动位置与目标节的位置关系
            if ($(target).length && $(target).offset().top <= scrollPos + 80) {
                // 移除所有导航链接的激活状态
                $('.ws-dir-ul li').removeClass('layui-this');
                // 为当前可见的目标节的导航链接添加激活状态
                $(this).addClass('layui-this');
            }
        });
        // 获取评论区的位置，如果到了评论区则取消所有导航的active
        const commentBlock = $('.ws-content .comment-text');
        if ($(commentBlock).length && $(commentBlock).offset().top <= scrollPos + 200) {
            // 移除所有导航链接的激活状态
            $('.ws-dir-ul li').removeClass('layui-this');
        }
    });
});

layui.use(function(){
    var carousel = layui.carousel;  // 轮播图
    var layer = layui.layer;  // 弹出层

    // 渲染 - 设置时间间隔、动画类型、宽高度等属性
    // 动态设置图片、轮播图的宽高
    var ratio = 1 / 5 * 2;
    var w = $("#images-carousel").parent().first().width();
    var h = w * ratio;
    var hpx = w * ratio + "px";
    $("#images-carousel img").width(w).height(h);
    var inst = carousel.render({
        elem: '#images-carousel',
        interval: 3600,
        anim: 'fade',
        width: w,
        height: h
    });
    $(document).ready(function(){
        $(window).resize(function(){
            w = $("#images-carousel").parent().first().width();
            h = w * ratio;
            hpx = w * ratio + "px";
            $("#images-carousel img").width(w).height(h);
            inst.reload({
                interval: 3600,
                anim: 'fade',
                width: w,
                height: h
            })
        });
    });

    // 文章图预览
    $(".ws-content .ws-center-detail img").on('click',function () {
        var imgSrc = $(this).attr('src');
        // 弹出层显示图片
        layer.open({
           type: 1,
           title: false,
           closeBtn: 0,
           shadeClose: true,
           content: '<img src="' + imgSrc + '"/>'
        });
    });

});