let log = console.log

$(function(){
    let camera = getQueryString('camera');
    let get_history_url = '/get_single_face_history?camera=' + camera;

    let oTable = new TableInit(get_history_url);
    oTable.Init();
    
})

function getQueryString(name) {
    let reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    let r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return unescape(r[2]);
    }
    return null;
}

function get_latest(){
    let latest_data = {
        "camera_id":getQueryString('camera')
    }
    $.post('/get_latest_single_face',data = latest_data,function(result){
        if (result) {
            $("#latest_person_picture").prop('src', result['person_picture'])
            $("#latest_face_train").prop('src', result['face_train'])
            $("#latest_face_capture").prop('src', result['face_capture'])
            $("#latest_camera_id").text(result['camera_id'])
            $("#latest_position").text(result['description'])
            $("#latest_time").text(result['time'])
            $("#latest_person_name").text(result['person_name'])
            $("#latest_person_id").text(result['person_id'])
            $("#latest_probability").text(result['probability'])
        }else{
            $("#latest_person_picture").prop('src', '')
            $("#latest_face_train").prop('src', '')
            $("#latest_face_capture").prop('src', '')
            $("#latest_camera_id").text('暂无数据')
            $("#latest_position").text('暂无数据')
            $("#latest_time").text('暂无数据')
            $("#latest_person_name").text('暂无数据')
            $("#latest_person_id").text('暂无数据')
            $("#latest_probability").text('暂无数据')
        }
    }) 
}

var timer = setInterval(get_latest,1000); 

$("#back_to_latest").click(function(){
    $("#history_div").hide(500) 
    $("#latest_div").show(300)
})

let queryParams = function(params){
    return {
        offset:params.offset,
        limit:params.limit
    }
}

let img_operateFormatter = function (value, row, index) {//赋予的参数
    return [
        '<button id="img_btn" class="btn btn-success" type="button">查看</button>',
    ].join('');
}

window.operateEvents = {
    "click #img_btn":function(e,value,row,index){
        let face_capture_url = row['face_capture'],
            face_train_url = row['face_train'],
            person_picture_url = row['person_picture'],
            person_name = row['person_name'],
            person_id = row['person_id'],
            probability = row['probability'];
        
        img_show(face_capture_url,face_train_url,person_picture_url,person_name,person_id,probability)
    }
}

function img_show(face_capture_url,face_train_url,person_picture_url,person_name,person_id,probability){
    $("#latest_div").hide(300)
    $("#history_div").show(300)
    let face_capture = $("#face_capture_history"),
        face_train = $("#face_train_history"),
        person_picture = $("#person_picture_history");

    person_picture.prop('src',person_picture_url)
    face_capture.prop('src',face_capture_url)
    face_train.prop('src',face_train_url)

    $("#history_person_name").text(person_name)
    $("#history_person_id").text(person_id)
    $("#history_probability").text(probability)

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
                field:'person_name',
                title:'姓名'
            },{
                field:'img_button',
                title:'图片',
                formatter:img_operateFormatter,
                events: operateEvents
            }]
        });
    };
    return oTableInit;
}