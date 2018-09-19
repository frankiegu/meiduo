let log = console.log;

let latest_data = {
    "camera_id":''
}

$(function(){
    let oTable = new TableInit();
    oTable.Init();
    // $('.pull-right.search input').val('abnormal');
})

$('.list-group-item').click(function(){
    $(this).addClass('list-active').siblings('li').removeClass('list-active')
})

function get_latest(latest_data){
    $.post('/get_latest_panel',data = latest_data,function(result){
        log(result)
        if (result) {
            $("#latest_img").attr('src', result['img_url']);            
            $("#latest_camera_id").text(result['camera_id']);
            $("#latest_time").text(result['time']);
            $("#latest_position").text(result['description']);
            $("#latest_alarm_type").text(result['alarm_type']);
            $("#latest_status_type").text(result['status_type'])
            $("#more_data").html(result['table']) 
        }else{
            $("#latest_img").attr('src', '');
            $("#latest_camera_id").text('暂无数据');
            $("#latest_time").text('暂无数据');
            $("#latest_position").text('暂无数据');
            $("#latest_alarm_type").text('暂无数据')
            $("#latest_status_type").text('暂无数据')
            $("#more_data").html('')
        }
    }) 
}

let timer = setInterval(function(){get_latest(latest_data);},1000); 

$(".list-group-item").each(function(index){
    $(this).click(function(){
        $("#history_div").hide(300)
        $("#latest_div").show(300)
        latest_data = {
            "camera_id":$(this).attr('id') || ''
        } 
        get_latest(latest_data);
    })
});


let queryParams = function(params){
    return {
        offset:params.offset,
        limit:params.limit,
        search:params.search
    }
}

// $("#normal_btn").click(function(e){
//     $('.pull-right.search input').val('abnormal');
//     log($('.pull-right.search input').val())
//     // $("#history").bootstrapTable('refresh');
// })

let data_operateFormatter = function (value, row, index) {//赋予的参数
    return [
        '<button id="data_btn" class="btn btn-success" type="button"><span class="glyphicon glyphicon-th-list"></span>查看</button>',
    ].join('');
}

// 点击查看图片和上传当前人脸的鼠标事件
window.operateEvents = {
    "click #data_btn":function(e,value,row,index){
        img_show(row['img_url'],row['table'])
    }
}

let TableInit = function(){
    let oTableInit = new Object();
    oTableInit.Init = function(){
        $("#history").bootstrapTable({
            url:'/get_panel_history',
            method:'get',
            dataType: "json",
            striped:true,
            cache:false,
            toolbar:'#toolbar',
            undefinedText: "空",
            pagination:true,
            sortable:false,
            sortOrder:"desc",
            sidePagination:"server",
            pageNumber:1,
            pageSize:8,
            pageList:[8,10,15],
            paginationPreText: '‹',//指定分页条中上一页按钮的图标或文字,这里是<
            paginationNextText: '›',//指定分页条中下一页按钮的图标或文字,这里是>
            paginationLoop:false,
            search:true,
            data_local: "zh-US",//表格汉化
            showRefresh:true,
            queryParams:queryParams,
            // customSearch:function(text){
            //     log(this.data)
            // },
            formatSearch: function () {
                return "按状态搜索";
            },
            columns:[{
                field:'camera_id',
                title:'相机id'
            },{ 
                field:'description',
                title:'相机位置'
            },{
                field:'time',
                title:'检测时间'
            },{
                field:'alarm_type',
                title:'报警类型'
            },{
                field:'status_type',
                title:'状态'
            },{
                field:'data_button',
                title:'数据',
                formatter:data_operateFormatter,
                events: operateEvents
            }]
        });
    };
    return oTableInit;
}

function img_show(img,table){
    $('.list-group-item').removeClass('list-active')
    $("#latest_div").hide(300)
    $("#history_div").show(300)
    $("#history_img").prop('src',img)
    $("#history_more_data").html(table)
}

