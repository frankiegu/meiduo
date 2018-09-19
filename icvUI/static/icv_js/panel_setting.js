let log = console.log

let points = [],
    panel_ori = [];

let flag = false; //矩形判断标志

let canvas = $("#canvas")[0],
    ctx = canvas.getContext('2d');

let img_w_px = 1920, //图片像素，用于坐标变换
    img_h_px = 1080; //图片像素，用于坐标变换

let $img = $("#canvas_img");

$(function(){
    let oTable = new TableInit();
    oTable.Init();
    let selected_opt = $("#camera_select option:selected").val() || "";
    $.post("/panel_first_frame",{"camera_id":selected_opt},function(result){
        if (result) {
            $img.attr('src',result['img_url'])
        }else{
            $img.attr('src','')
        }
    })
})


function draw_pic(){
    ctx.drawImage($img[0],0,0,canvas.width,500);
}

// canvas 自适应
function resizeCanvas(){
    clear_draw();
    $("#canvas").attr('width',parseInt($("#canvas_box").width()*0.9));
    draw_pic();
}

resizeCanvas();
$(window).resize(resizeCanvas);

// 清空画布
function clear_draw(){
    canvas.height = canvas.height
    points = [];
	panel_ori = [];
}

$("#camera_select").change(function(e){
    let selected_opt = $("#camera_select option:selected").val() || "";
    $.post("/panel_first_frame",{"camera_id":selected_opt},function(result){
        if (result) {
            $img.attr('src',result['img_url'])
        }else{
            $img.attr('src','')
        }
    })
    clear_draw();
    draw_pic();
})

$("#clera_ori").click(function(e){
    clear_draw();
    draw_pic();
})

$("#post_data").click(function(e){
    if (panel_ori.length === 0) {
        alert('你还没有进行标注');
        return ;
    }else if($("#camera_select option:selected").val() === ''){
        alert('你还没有选择相机');
        return ;
    }

    for(let i = 0;i < panel_ori.length; i++){
        let ori = panel_ori[i]['ori_data']
        if (ori.length != 2) {
            alert('标注过程中鼠标不可越过画面区域，请刷新画面并重画')
            panel_ori = []
            return ;
        }
        for (let j = 0;j < ori.length;j++){
            let x = ori[j][0],
                y = ori[j][1];
            ori[j][0] = parseInt((img_w_px * x)/canvas.width);
            ori[j][1] = parseInt((img_h_px * y)/canvas.height);    
        }
    }

    let selected_opt = $("#camera_select option:selected").val();
    data = {
        "camera_id":selected_opt,
        "ori_data":JSON.stringify(panel_ori)
    }

    $.post('/update_panel',data,function(result){
        panel_ori = [];
        resizeCanvas();
        if (result === 'ok') {
            successful_operation(); 
            $("#panel_table").bootstrapTable('refresh');
        }else{
            alert('提交失败');
        }
    })
})

// 画矩形
function draw_rect(panel_ori){
    ctx.beginPath();
    ctx.strokeStyle = 'blue';
    ctx.fillStyle = 'red';
    ctx.font = "26px Arial";
    for(let i = 0; i < panel_ori.length; i++){
        let start_x = panel_ori[i]['ori_data'][0][0],
            start_y = panel_ori[i]['ori_data'][0][1],
            end_x = panel_ori[i]['ori_data'][1][0],
            end_y = panel_ori[i]['ori_data'][1][1],
            name = panel_ori[i]['name'];
        ctx.strokeRect(start_x,start_y,end_x - start_x,end_y-start_y);
        ctx.fillText(name,start_x + 10,start_y + 10);
    }
}

$("#canvas").mousedown(function(e){
    flag = true;
    let down_x = e.offsetX,
        down_y = e.offsetY;
    points.push([down_x, down_y])  
})
.mouseup(function(e){
    flag = false;
    let up_x = e.offsetX,
        up_y = e.offsetY;
    points.push([up_x,up_y])
    $("#panel_modal").modal("toggle");
})
.mousemove(function(e){
    if(flag){
        canvas.height = canvas.height
        draw_pic();
        draw_rect(panel_ori)
        ctx.strokeRect(points[0][0], points[0][1], e.offsetX-points[0][0],e.offsetY-points[0][1]);
    }
})

// 选择类型
$("#label_confirm").click(function(e){
    let label = $("#rect_label option:selected")
    let name = $("#rect_name").val()
    if (name == '') {
        alert('你还没输入区域名称')
        return ;
    } 
    ctx.fillStyle = 'red';
    ctx.font = "26px Arial";
    ctx.fillText(name,points[0][0] + 10,points[0][1] + 10);
	panel_ori.push({
        "name":name,
		"label":label.val(),
		"ori_data":points
    });
	points = [];
	$("#panel_modal").modal("toggle");
});

$('#panel_modal').on('hidden.bs.modal', function () {
    $("#rect_name").val('')
    canvas.height = canvas.height
    draw_pic();
    draw_rect(panel_ori);
    points = [];
})


let TableInit = function(){
    let oTableInit = new Object();
    oTableInit.Init = function(){
        $("#panel_table").bootstrapTable({
            url:'/get_panel_ori',
            method:'get',
            dataType: "json",
            striped:true,
            cache:false,
            undefinedText: "空",
            pagination:true,
            sortable:false,
            sortOrder:"desc",
            sidePagination:"client",
            pageNumber:1,
            pageSize:8,
            pageList:[4,8,12,20],
            paginationPreText: '‹',//指定分页条中上一页按钮的图标或文字,这里是<
            paginationNextText: '›',//指定分页条中下一页按钮的图标或文字,这里是>
            data_local: "zh-US",//表格汉化
            showRefresh:true,
            columns:[{
                field:'camera_id',
                title:'面板相机id'
            },{ 
                field:'ori_data',
                title:'面板参数'
            },{
                field:'description',
                title:'描述'
            }
        ]
        });
    };
    return oTableInit;
}

$("#restart_panel_btn").click(function(e){
    $.post('/restart_panel',data = {"status":"restart"},function(result){
        if (result == 'ok') {
            successful_operation()
            alert('操作成功，请选择相机并点击刷新获取画面.')
        }else{
            alert('操作失败')
        }
    })
})

// 日常拍照时间间隔
$("#save_time").click(function(e){
    let interval = $("#time_select option:selected").val();
    let interval_text = $("#time_select option:selected").text();
    $.post("/update_interval",data = {"interval":interval.split('_')[1]},function(result){
        if (result == 'ok') {
            successful_operation()
            $("#interval_box").text(interval_text)
            alert('操作成功，日常拍照时间间隔将应用到所有相机')
        }else{
            alert('操作失败')
        }
    })

})