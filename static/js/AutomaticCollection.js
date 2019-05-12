/* 360 自动收录 */
(function(){
var src = (document.location.protocol == "http:") ? "http://js.passport.qihucdn.com/11.0.1.js?2f8b45c478390cf991af76cce5ee7581":"https://jspassport.ssl.qhimg.com/11.0.1.js?2f8b45c478390cf991af76cce5ee7581";
document.write('<script src="' + src + '" id="sozz"><\/script>');
})();

/* 百度 自动收录 */
(function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {
        bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
    }
    else {
        bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();
