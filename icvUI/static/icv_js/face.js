let log = console.log

let latest_data = {
    "camera_id":''
}

$(function(){
    let oTable = new TableInit();
    oTable.Init();
})

$('.list-group-item').click(function(){
    $(this).addClass('list-active').siblings('li').removeClass('list-active')
})

function get_latest(latest_data){
    $.post('/get_latest_face',data = latest_data,function(result){
        // log(result['description'])
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

let timer = setInterval(function(){get_latest(latest_data);},1000);

$(".list-group-item").each(function(index){
    $(this).click(function(){
        $("#latest_div").show(300)
        $("#history_div").hide(500)
        latest_data = {
            "camera_id":$(this).attr('id') || ''
        } 
        get_latest(latest_data);     
    })
});


let queryParams = function(params){
    return {
        offset:params.offset,
        limit:params.limit
    }
}

//自定义操作
let upload_operateFormatter = function (value, row, index) {//赋予的参数
    return [
        '<button id="upload_btn" class="btn btn-primary" type="button" data-target="#upload_modal" data-toggle="modal"><span class="glyphicon glyphicon-upload" aria-hidden="true"></span></button>',
    ].join('');
}

let img_operateFormatter = function (value, row, index) {//赋予的参数
    return [
        '<button id="img_btn" class="btn btn-success" type="button"><span class="glyphicon glyphicon-picture"></span></button>',
    ].join('');
}

// 点击查看图片和上传当前人脸的鼠标事件
window.operateEvents = {
    "click #img_btn":function(e,value,row,index){
        let face_capture_url = row['face_capture'],
            face_train_url = row['face_train'],
            person_picture_url = row['person_picture'],
            person_name = row['person_name'],
            person_id = row['person_id'],
            probability = row['probability'];

        img_show(face_capture_url,face_train_url,person_picture_url,person_name,person_id,probability)

    },

    "click #upload_btn":function(e,value,row,index){
        let face_capture_url = row['face_capture']
        $("#upload_face_capture").attr('src',face_capture_url)
    }
}

$('#upload_modal').on('hide.bs.modal', function () {
    $("#upload_person_name").val('')
    $("#upload_person_id").val('')
})


$("#upload_confirm").click(function(e){
    let upload_person_name = $.trim($("#upload_person_name").val())
    let upload_person_id = $.trim($("#upload_person_id").val())
    let upload_face_capture = $("#upload_face_capture").attr('src')
    
    let reg = /^[0-9]{8}$/;

    if (upload_person_name === '' || upload_person_id === '') {
        alert('请填写参数')
        return ;
    }else if (!reg.test(upload_person_id)) {
        alert('请填写8位数字的ID')
        return ;
    }

    upload_data = {
        "person_name":upload_person_name,
        "person_id":upload_person_id,
        "face_train":upload_face_capture
    }

    $.ajax({
        url:'/upload_face_capture',
        type: 'POST',
        data: upload_data,
        beforeSend:function(XMLHttpRequest){
            ajax_loading()
        }, 
        success:function (returndata) {
            if(returndata === 'ok'){
                $("#upload_modal").modal("toggle");
                ajax_ok()
                successful_operation();
                // $.post('/restart_face',data = {"status":"restart"},function(result){
                //     if (result == 'ok') {
                //         alert('操作成功');
                //     }else{
                //         alert('操作失败');
                //     }
                // })
            }else{
                ajax_ok()
                alert(returndata);
            }
    　　}, 
    　　error: function (returndata) {
            ajax_ok()
            alert("上传失败！")
        }
    })
})


function img_show(face_capture_url,face_train_url,person_picture_url,person_name,person_id,probability){
    $('.list-group-item').removeClass('list-active')
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


let TableInit = function(){
    let oTableInit = new Object();
    oTableInit.Init = function(){
        $("#history").bootstrapTable({
            url:'/get_face_history',
            method:'get',
            dataType: "json",
            striped:true,
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
            },
            // {
            //     field:'person_id',
            //     title:'个人ID'
            // },{
            //     field:'probability',
            //     title:'相似度'
            // },
            {
                field:'img_button',
                title:'图片',
                formatter:img_operateFormatter,
                events: operateEvents
            },{
                field:'button',
                title:'录入当前人脸',
                formatter:upload_operateFormatter,
                events: operateEvents
            }]
        });
    };
    return oTableInit;
}

