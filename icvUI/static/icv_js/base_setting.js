var log = console.log

$(function(){
    var oTable = new TableInit();
    oTable.Init();
})


//自定义操作
var operateFormatter = function (value, row, index) {//赋予的参数
    return [
        '<button id="modify_btn" class="btn btn-warning" type="button" data-target="#modify_modal" data-toggle="modal"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>修改内容</button>',
    ].join('');
}

// 修改按钮
window.operateEvents = {
    "click #modify_btn":function(e, value, row, index){
        let camera_id = row['camera_id'],
            camera_ip = row['camera_ip'],
            application = row['application'],
            description = row['description'];

        $("#camera_id_input").val(camera_id);
        $("#camera_ip_input").val(camera_ip);
        $("#description_input").val(description);
        
        if (application) {
            let application_setting = application.split(',') //获取已设置好的功能内容
            let app_select = $("#application_box .checkbox ") //checkbox父元素数组，用于获取text
            let input_selected = $("#application_box .checkbox input") //input数组
            for(let i = 0; i < app_select.length; i++){
                let selected = $.trim($(app_select[i]).text())
                if ($.inArray(selected,application_setting) >= 0) {
                    $(input_selected[i]).prop('checked',true)
                }
            } 
        }
    }
}

$("#modify_confirm").click(function(e){
    let application_array = [];
    $.each($('#application_box input:checkbox:checked'),function(){
        application_array.push($(this).val())
    });

    application = application_array.join(",")

    let camera_id = $.trim($("#camera_id_input").val()),
        camera_ip = $.trim($("#camera_ip_input").val()),
        description = $.trim($("#description_input").val());

    if (application === '' || description === '') {
        alert('你还有未填写的参数');
        return ;
    }
    
    let data = {
        "camera_id":camera_id,
        "camera_ip":camera_ip,
        "application":application,
        "description":description
    }

    $.post('/update_camera', data = data, function(result){
        log(data)
        if (result == 'ok') {
            $("#modify_modal").modal("toggle");
            successful_operation();
            $("#base_setting_table").bootstrapTable('refresh');	
        }else{
            alert(result);
        }
    })
})


$("#add_confirm").click(function(e){
    new_camera_id = $("#new_camera_id").val()
    new_camera_ip = $("#new_camera_ip").val()

    let id_reg = /camera\d+/
    let ip_reg = /192\.168\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9])\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9])/
    
    if (new_camera_id === '' || new_camera_ip === '') {
        alert('你还有未填写的参数')
        return ;
    }else if (!id_reg.test(new_camera_id)) {
        alert('请输入正确id格式，如camera1，camera2')
        return ;
    }else if(!ip_reg.test(new_camera_ip)){
        alert('请输入正确ip格式---192.168.X.X，如192.168.1.101')
        return ;
    }

    data = {
        "camera_id":new_camera_id,
        "camera_ip":new_camera_ip
    }

    $.post('/add_new_camera',data = data, function(result){
        if (result === 'ok') {
            $("#add_camera_modal").modal("toggle");
            successful_operation();
            $("#base_setting_table").bootstrapTable('refresh');	         
        }else if(result === 'wrong'){
            alert('提交失败')
        }else{
            alert(result)
        }
    })
})

$('#add_camera_modal').on('hide.bs.modal', function () {
    $("#new_camera_id").val('')
    $("#new_camera_ip").val('')
})

$('#modify_modal').on('hide.bs.modal', function () {
    let input_selected = $("#application_box .checkbox input")
    for(let i = 0;i < input_selected.length;i++){
        $(input_selected[i]).prop('checked',false)
    }

})

var TableInit = function(){
    var oTableInit = new Object();
    oTableInit.Init = function(){
        $("#base_setting_table").bootstrapTable({
            url:'/get_camera',
            method:'get',
            dataType: "json",
            striped:true,
            cache:false,
            undefinedText: "空",
            toolbar:'#toolbar',
            pagination:true,
            sortable:false,
            sortOrder:"desc",
            sidePagination:"client",
            pageNumber:1,
            pageSize:8,
            pageList:[4,8,12],
            paginationPreText: '‹',//指定分页条中上一页按钮的图标或文字,这里是<
            paginationNextText: '›',//指定分页条中下一页按钮的图标或文字,这里是>
            data_local: "zh-US",//表格汉化
            showRefresh:true,
            columns:[
            {
                checkbox: true
            },{
                field:'camera_id',
                title:'相机id'
            },{ 
                field:'camera_ip',
                title:'相机ip'
            },{
                field:'application',
                title:'功能'
            },{
                field:'description',
                title:'描述'
            },{
                field:'button',
                title:'操作',
                formatter:operateFormatter,
                events: operateEvents
            }
        ]
        });
    };
    return oTableInit;
}


//选中可用删除按钮
$("#base_setting_table").on('check.bs.table check-all.bs.table uncheck.bs.table uncheck-all.bs.table', function (e, row,ele) {
    var row_data = $('#base_setting_table').bootstrapTable('getSelections');
    if (row_data.length != 0) {
        $("#del_camera_btn").removeAttr('disabled');
    }else{
        $("#del_camera_btn").attr('disabled','disabled');
    }
});


// 删除按钮触发
$("#del_camera_btn").click(function () {
    let row_data = $('#base_setting_table').bootstrapTable('getSelections');//获取选择行数据 返回列表
	let del_camera = []
	for (var i = 0; i < row_data.length; i++) {//循环读取选中行数据
		del_camera.push({
            camera:row_data[i]['camera_id']
        })
	}

	$("#del_camera_body").html(function(){
		let result = '<p style="font-size:20px;">删除后相关数据将无法恢复。确定要删除吗?</p>'
		for (var i = 0; i < del_camera.length; i++) {
			result += "<h3 style='display:inline-block;margin-left:8px;'> <span class='label label-default' style='margin-left:5px;'>"+ del_camera[i]['camera'] + "</span></h3>"; 		
		}
		return result
	})     
})


//删除确认按钮触发
$("#del_confirm").click(function(){
	let row_data = $('#base_setting_table').bootstrapTable('getSelections');

	let del_camera = []
	for (var i = 0; i < row_data.length; i++) {
		del_camera.push(row_data[i]['camera_id'])
	}
    
    data = {"del_camera":JSON.stringify(del_camera)}
	$.post('/del_camera',data,function(result){
        // log(result)
    	if (result == "ok") {		            		
            $("#del_camera_modal").modal("toggle");
            $("#del_camera_btn").attr('disabled','disabled');
            successful_operation()
            $("#base_setting_table").bootstrapTable('refresh');	
    	}else{
            $("#del_camera_btn").attr('disabled','disabled');
    		alert('删除失败');
    	}
	});
});