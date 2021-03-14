$(function() {
    //通用头部搜索切换
    $('#search-hd .search-input').on('input propertychange', function() {
        var val = $(this).val();
        if (val.length > 0) {
            $('#search-hd .pholder').hide(0);
        } else {
            var index = $('#search-bd li.selected').index();
            $('#search-hd .pholder').eq(index).show().siblings('.pholder').hide(0);
        }
    })
    $('#search-bd li').click(function() {
        var index = $(this).index();
        $('#search-hd .pholder').eq(index).show().siblings('.pholder').hide(0);
        $('#search-hd .search-input').eq(index).show().siblings('.search-input').hide(0);
        $(this).addClass('selected').siblings().removeClass('selected');
        $('#search-hd .search-input').val('');
    });
})