let log = console.log

$(function(){
    let camera = getQueryString('camera');
    let get_history_url = '/get_single_safedress_history?camera=' + camera;
     
    let oTable = new TableInit(get_history_url);
    oTable.Init();    
})


function get_latest(){
    let latest_data = {
        "camera_id":getQueryString('camera')
    }
    $.post('/get_latest_single_safedress',data = latest_data,function(result){
        if (result) {
            $("#latest_img").prop('src', result['img_url']);            
            $("#latest_camera_id").text(result['camera_id']);
            $("#latest_time").text(result['time']);
            $("#latest_position").text(result['description']);
            $("#latest_alarm_type").text(result['alarm_type']);
        }else{
            $("#latest_img").prop('src', '');            
            $("#latest_camera_id").text('暂无数据');
            $("#latest_time").text('暂无数据');
            $("#latest_position").text('暂无数据');
            $("#latest_alarm_type").text('暂无数据');
        }
    }) 
}

var timer = setInterval(function(){get_latest();},1000); 

function getQueryString(name) {
    let reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    let r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return unescape(r[2]);
    }
    return null;
}


let img_operateFormatter = function (value, row, index) {//赋予的参数
    return [
        '<button id="img_btn" class="btn btn-success" type="button">查看</button>',
    ].join('');
}

let queryParams = function(params){
    return {
        offset:params.offset,
        limit:params.limit
    }
}

window.operateEvents = {
    "click #img_btn":function(e,value,row,index){
        let all_data = $("#history").bootstrapTable('getData',useCurrentPage=true);
        let img_list = new Array()
        for(let i = 0; i < all_data.length; i++){
            img_list.push(all_data[i]['img'])
        }
        $.pictureViewer({
            images: img_list, //需要查看的图片，数据类型为数组
            initImageIndex: index + 1, //初始查看第几张图片，默认1
        });

    }
}

let TableInit = function(url){
    let oTableInit = new Object();
    oTableInit.url = url
    oTableInit.Init = function(){
        $("#history").bootstrapTable({
            url:oTableInit.url,
            method:'get',
            dataType: "json",
            striped:true,
            toolbar:"#toolbar",
            cache:false,
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
            data_local: "zh-US",//表格汉化
            showRefresh:true,
            queryParams:queryParams,
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
                field:"alarm_type",
                title:"报警类型"
            },
            {
                field:'img_button',
                title:'图片',
                formatter:img_operateFormatter,
                events: operateEvents
            }]
        });
    };
    return oTableInit;
}