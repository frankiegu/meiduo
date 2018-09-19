var log = console.log

var points = [],
    intrusion_ori = [];

var canvas = $("#canvas")[0],
    ctx = canvas.getContext('2d');

var img_w_px = 1920, //图片像素，用于坐标变换
    img_h_px = 1080; //图片像素，用于坐标变换

var $img = $("#canvas_img");

$(function(){
    var oTable = new TableInit();
    oTable.Init();
})


function draw_pic(){
    let selected_opt = $("#camera_select option:selected").val() || "";
    $.post("/intrusion_first_frame",{"camera_id":selected_opt},function(result){
        if (result) {
            $img.attr('src',result['img_url'])
            ctx.drawImage($img[0],0,0,canvas.width,500);
        }else{
            $img.attr('src','')
            ctx.drawImage($img[0],0,0,canvas.width,500);
        }
    })
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
	intrusion_ori = [];
}

$("#camera_select").change(function(e){
    clear_draw();
    draw_pic();
})

$("#clera_ori").click(function(e){
    clear_draw();
    draw_pic();
})

$("#post_data").click(function(e){
    if (intrusion_ori.length === 0) {
        alert('你还没有画越界区域');
        return ;
    }else if($("#camera_select option:selected").val() === ''){
        alert('你还没有选择相机');
        return ;
    }
    for(let i = 0;i < intrusion_ori.length; i++){
        let x = intrusion_ori[i][0],
            y = intrusion_ori[i][1];
        intrusion_ori[i][0] = parseInt((img_w_px * x)/canvas.width);
        intrusion_ori[i][1] = parseInt((img_h_px * y)/canvas.height);
    }

    let selected_opt = $("#camera_select option:selected").val();
    data = {
        "camera_id":selected_opt,
        "ori_data":JSON.stringify(intrusion_ori)
    }

    $.post('/update_intrusion',data,function(result){
        intrusion_ori = [];
        resizeCanvas();
        if (result === 'ok') {
            successful_operation(); 
            $("#intrusion_table").bootstrapTable('refresh');
        }else{
            alert('提交失败');
        }
    })
})

function draw_one_circle(x,y,r,color){
    ctx.globalAlpha = 0.85;
    ctx.arc(x,y,r,0,2*Math.PI);
    ctx.fillStyle = color;
    ctx.strokeStyle = "black";
}

function draw_all_circles(points){
    for(var i = 0;i < points.length; i++){
         var circle = points[i];
         ctx.beginPath();
         if(i === 0){
             draw_one_circle(circle[0],circle[1],7,'green');
         }else{
             draw_one_circle(circle[0],circle[1],5,'red'); 
         }
         ctx.fill();
         ctx.stroke();
     } 
}


function draw_all_lines(points) {
    ctx.beginPath();
    ctx.lineWidth = 2;
    ctx.fillStyle = "rgba(100%,50%,0%,0.3)";
    ctx.strokeStyle = "#9d4dca";
    ctx.moveTo(points[0][0],points[0][1]);
    for(var i = 1;i < points.length; i++){
        ctx.lineTo(points[i][0],points[i][1]);
    }
    ctx.stroke();
}


$("#canvas").mousedown(function(e){
    if (e.which == 1) {
        var down_x = e.offsetX,
            down_y = e.offsetY;
        
        if (intrusion_ori.length != 0) {
            return ;
        }
        for(let i = 1; i < points.length; i++){
            let a = down_x - points[0][0],
                b = down_y - points[0][1];
            
            let distance = Math.sqrt(Math.pow(a,2) + Math.pow(b,2));
            if (distance <= 7) {
                ctx.closePath();
                ctx.stroke();
                ctx.fill();
                intrusion_ori = points;
                points = [];
                return ;
            }
        }
       
        points.push([down_x,down_y]);
        draw_all_circles(points);
        draw_all_lines(points);
    }
})


var TableInit = function(){
    var oTableInit = new Object();
    oTableInit.Init = function(){
        $("#intrusion_table").bootstrapTable({
            url:'/get_intrusion_ori',
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
                title:'越界相机id'
            },{ 
                field:'ori_data',
                title:'越界参数'
            },{
                field:'description',
                title:'描述'
            }
        ]
        });
    };
    return oTableInit;
}

$("#restart_intrusion_btn").click(function(e){
    $.post('/call_intrusion_first',data = {"status":"restart"},function(result){
        if (result == 'ok') {
            successful_operation()
            alert('操作成功，请选择相机并点击刷新获取画面.')
        }else{
            alert('操作失败')
        }
    })
})