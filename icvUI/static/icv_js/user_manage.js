
// 新增用户按钮触发事件
$("#btn_add_user").click(function(){
	//每次点击新增用户先清除表单数据
	$("#username").val("");
	$("#usercode").val("");
	$("#password").val("");
	$("#password_confirm").val("");
	$("#add_tips").html("");
	$("#add_tips").val("");
});


// 添加用户提交按钮触发事件
$("#adduser_confirm").click(function(e){
	//获取用户填写的参数
	$("#add_tips").html("");
	username = $("#username").val(); //用户姓名，中文那个
	usercode = $("#usercode").val(); //用户账号，英文那个
	password = $("#password").val();
	password_confirm = $("#password_confirm").val();
	role = $("#role").val();
	userfrom = $("#userfrom").val();

    var myReg = /^[a-zA-Z0-9_]{0,}$/; //验证用户名是否有非法字符

    if (!myReg.test(usercode)) {
    	$("#add_tips").html("用户账号不能含有中文，空格等非法字符");
    }else if (!username || !usercode || !password || !password_confirm) {
		$("#add_tips").html("请填写完整数据");
	}else if (password != password_confirm || password.length < 6) {
		$("#add_tips").html("密码信息错误");
	}else{ //符合规则，提交请求
		data = {
			username:username,
			usercode:usercode,
			password:password,
			role:role,
			userfrom:userfrom
		}

		//ajax提交post请求
		$.post('/useradd', data, function (result) {
			if (result == 'right') {
				$("#add_modal").modal("toggle");
				$("#alert_box").show(300);
				$('#alert_box').delay(800).hide(300);				
				$("#table_server").bootstrapTable('refresh');			
			}else{
				$("#add_tips").html("添加失败");
			}
		});
	}
	// return e.preventDefault();
})

// table传参
var queryParams = function(params){
    return {        //这里的params是table提供的
                offset: params.offset,//从数据库第几条记录开始
                limit: params.limit,//找多少条
                search: params.search
            };
}

//自定义操作
var operateFormatter = function (value, row, index) {//赋予的参数
      return [
          '<button id="modify_user" class="btn btn-info" type="button" data-target="#modify_modal" data-toggle="modal"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>修改信息</button>',
          '<button id="modify_pwd" class="btn btn-warning" type="button" data-target="#modpwd_modal" data-toggle="modal" ><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>更改密码</button>'
      ].join('');
}

// 修改用户按钮触发事件
window.operateEvents = {
	"click #modify_user":function(e,value,row,index){
		role = row['role']
		userfrom = row['group_name']
		username = row['user_name']
		usercode = row['user_code']
		// console.log(role,userfrom,username,usercode)
		$('#modrole option').filter(function(){return $(this).text()==role;}).attr("selected",true);
		$('#moduserfrom option').filter(function(){return $(this).text()==userfrom;}).attr("selected",true);	
		$("#modusername").val(username)
		$("#modusercode").val(usercode)
		// $('#modify_modal').on('hide.bs.modal', function () {
		//        	$('#modrole option').filter(function(){return $(this).text()==role;}).attr("selected",false);
		// 		$('#moduserfrom option').filter(function(){return $(this).text()==userfrom;}).attr("selected",false);
		// 		// $("#table_server").bootstrapTable('refresh');	
		// });

	},

	"click #modify_pwd":function(e,value,row,index){
		username = row['user_name']
		usercode = row['user_code']
		$("#modpwdusername").val(username)
		$("#modpwdusercode").val(usercode)
		$("#modpwd_tips").html("");
	},
}

//提交修改触发事件
$("#modify_confirm").click(function (e) {
			role = $("#modrole").val();
			userfrom = $("#moduserfrom").val();
			username = $("#modusername").val()
			usercode = $("#modusercode").val()
			data = {
				role:role,
				userfrom:userfrom,
				username:username,
				usercode:usercode
			}
			$.post('/usermodify',data,function(result){
				if (result == 'right') {
					$("#modify_modal").modal("toggle");
					$("#alert_box").show(300);
					$('#alert_box').delay(800).hide(300);				
					$("#table_server").bootstrapTable('refresh');					
				}else{
					$("#modify_modal").modal("toggle");
					alert('修改失败');
					$("#table_server").bootstrapTable('refresh');
				}
		});
})

// 删除按钮触发
$("#btn_delete_user").click(function () {
	var row_data = $('#table_server').bootstrapTable('getSelections');//获取选择行数据 返回列表
	$("#delete_modal").modal("toggle");
	var delete_user = []
	for (var i = 0; i < row_data.length; i++) {//循环读取选中行数据
		delete_user.push({
								username:row_data[i]['user_name'],
								userfrom:row_data[i]['group_name']
							})
	}

	$("#delete_modal_body").html(function(){
		let result = '<p>确定要删除以下用户吗?</p>'
		for (var i = 0; i < delete_user.length; i++) {
			result += "<h3 style='display:inline-block;margin-left:8px;'> <span class='label label-default' style='margin-left:5px;'>"+ delete_user[i]['userfrom'] + ":" + delete_user[i]['username'] + "</span></h3>"; 		
		}
		return result
	})     
})

//删除确认按钮触发
$("#delete_confirm").click(function(){
	var row_data = $('#table_server').bootstrapTable('getSelections');

	del_user_code = []
	for (var i = 0; i < row_data.length; i++) {
		del_user_code.push(row_data[i]['user_code'])
	}

	del_data = del_user_code.join(',')
	data = {del_users:del_data}

	$.post('/userdelete',data,function(result){
    	if (result == "right") {		            		
			$("#delete_modal").modal("toggle");
			// $("#btn_delete_user").attr('disabled','disabled');
			$("#alert_box_text").html("操作成功,将刷新页面..."); //添加文本
			$("#alert_box").show(300);
			$('#alert_box').delay(800).hide(300);
			$("#table_server").bootstrapTable('refresh');
			setTimeout(function(){window.location.reload();},900);	
    	}else{
    		$("#delete_modal").modal("toggle");
    		$("#btn_delete_user").attr('disabled','disabled');
    		alert('删除失败');
			$("#table_server").bootstrapTable('refresh');
    	}
	});
});


//修改密码确认按钮
$("#modpwd_confirm").click(function(e,value,row,index){
	username = $("#modpwdusername").val()
	usercode = $("#modpwdusercode").val()
	password = $("#modpassword").val();
	password_confirm = $("#modpassword_confirm").val();
	if (password != password_confirm || password.length < 6 ) {
		$("#modpwd_tips").html("密码信息错误");
	}else{
		data = {
			usercode:usercode,
			password:password
		}
		$.post('/passwordmod',data,function(result){
			if (result == 'right') {
				$("#modpwd_modal").modal("toggle");
				$("#alert_box_text").html("操作成功,请重新登录"); //添加文本
				$("#alert_box").show(300);
				$('#alert_box').delay(800).hide(300);				
				$("#table_server").bootstrapTable('refresh');
				// $.get('/logout',function(){}) //释放当前session
			}else{
				$("#modpwd_modal").modal("toggle");
				alert('修改失败');
				$("#table_server").bootstrapTable('refresh');
			}
		})
	}


});


$(function(){
    var t = $("#table_server").bootstrapTable('destroy').bootstrapTable({
        url: '/get_user_data',
        method: 'get',
        dataType: "json",
        toolbar: '#toolbar',
        striped: true,//设置为 true 会有隔行变色效果
        undefinedText: "空",//当数据为 undefined 时显示的字符
		pagination: true, //分页
		showRefresh:true,
        paginationLoop:false,//设置为 true 启用分页条无限循环的功能。
        // showToggle: "true",//是否显示 切换试图（table/card）按钮
        showColumns: true,//是否显示 内容列下拉框
        pageNumber: 1,//如果设置了分页，首页所在的默认页码
        // showPaginationSwitch:true,//是否显示 数据条数选择框
        pageSize: 5,//如果设置了分页，页面数据条数
        pageList: [5,10,20,30,40],  //如果设置了分页，设置可供选择的页面数据条数。设置为All 则显示所有记录。
        paginationPreText: '‹',//指定分页条中上一页按钮的图标或文字,这里是<
        paginationNextText: '›',//指定分页条中下一页按钮的图标或文字,这里是>
        // singleSelect: false,//设置True 将禁止多选
        search: true, //显示搜索框
        data_local: "zh-US",//表格汉化
        sidePagination: "server", //服务端处理分页
        queryParams: queryParams,//自定义参数，这里的参数是传给后台的，我这是是分页用的
        // idField: "user_code",//指定主键列
        columns: [
            {
                checkbox: true
            },
            {
                title: '账号',
                field: 'user_code',
                align: 'center'
            },
            {
                title: '用户姓名',
                field: 'user_name',
                align: 'center'
            },
            {
                title: '用户角色',
                field: 'role',
                align: 'center'
            },
            {
                title: '用户归属',
                field: 'group_name',
                align: 'center'
            },
            // {
            //     title: '用户权限',
            //     field: 'user_limit',
            //     align: 'center'
            // },
            {
                title: '操作',
                field: 'button',
                align: 'center',
                formatter:operateFormatter,
                events: operateEvents
            }

        ],

    });


});

//选中可用删除按钮
$("#table_server").on('check.bs.table check-all.bs.table uncheck.bs.table uncheck-all.bs.table', function (e, row,ele) {
		var row_data = $('#table_server').bootstrapTable('getSelections');
		if (row_data.length != 0) {
			$("#btn_delete_user").removeAttr('disabled');
		}else{
			$("#btn_delete_user").attr('disabled','disabled');
		}
});


