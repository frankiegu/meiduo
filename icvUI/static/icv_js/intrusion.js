var log = console.log;

var latest_data = {
    "camera_id": ''
}

$(function () {
    var oTable = new TableInit();
    oTable.Init();
})

$('.list-group-item').click(function () {
    $(this).addClass('list-active').siblings('li').removeClass('list-active')
})

function get_latest(latest_data) {
    $.post('/get_latest_intrusion', data = latest_data, function (result) {
        if (result) {
            $("#latest_img").attr('src', result['img_url']);
            $("#latest_camera_id").text(result['camera_id']);
            $("#latest_time").text(result['time']);
            $("#latest_position").text(result['description']);
        } else {
            $("#latest_img").attr('src', '');
            $("#latest_camera_id").text('暂无数据');
            $("#latest_time").text('暂无数据');
            $("#latest_position").text('暂无数据');
        }
    })
}


var timer = setInterval(function () {
    get_latest(latest_data);
}, 1000);

$(".list-group-item").each(function (index) {
    $(this).click(function () {
        latest_data = {
            "camera_id": $(this).attr('id') || ''
        }
        get_latest(latest_data);
    })
});

var queryParams = function (params) {
    return {
        offset: params.offset,
        limit: params.limit
    }
}


var TableInit = function () {
    var oTableInit = new Object();
    oTableInit.Init = function () {
        $("#history").bootstrapTable({
            url: '/get_intrusion_history',
            method: 'get',
            dataType: "json",
            striped: true,
            cache: false,
            undefinedText: "空",
            pagination: true,
            sortable: false,
            sortOrder: "desc",
            sidePagination: "server",
            pageNumber: 1,
            pageSize: 8,
            pageList: [8, 10, 15],
            paginationPreText: '‹',//指定分页条中上一页按钮的图标或文字,这里是<
            paginationNextText: '›',//指定分页条中下一页按钮的图标或文字,这里是>
            paginationLoop: false,
            data_local: "zh-US",//表格汉化
            showRefresh: true,
            queryParams: queryParams,
            columns: [{
                field: 'camera_id',
                title: '相机id'
            }, {
                field: 'description',
                title: '相机位置'
            }, {
                field: 'time',
                title: '检测时间'
            }, {
                field: 'img_label',
                title: '图片'
            }],
            onClickRow: function (row, $element, field) {
                // var i = $element.data('index');//可通过此参数获取当前行号
                if (field === "img_label") {
                    let reg = /src="(.*)"/
                    let img_url = row['img_label'].match(reg)[1]
                    img_show(img_url)
                }
            }
        });
    };
    return oTableInit;
}

$("#big_img_box").click(function (e) {
    $("#big_img_box").fadeOut(300)
    $("#big_img_box").empty()
})

function img_show(img_url) {
    $("#big_img_box").fadeIn(300);
    let img = new Image();
    $img = $(img)
    $img.css('width', $(window).width() * 0.7).css('height', $(window).height() * 0.8)
    $img.css('position', 'absolute')
    $img.css('top', '50%').css('left', '50%')
    $img.css({marginLeft: (-$(window).width() * 0.7) / 2 + 'px', marginTop: (-$(window).height() * 0.8) / 2 + 'px'})
    $img.attr('src', img_url)
    $("#big_img_box").append(img)
}