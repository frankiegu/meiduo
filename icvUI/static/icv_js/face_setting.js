var log = console.log

$(function(){
    let oTable = new TableInit();
    oTable.Init();
})

$("#face_input_btn").click(function(e){
    let form_data = new FormData($('#uploadForm')[0]);
    let person_name = $.trim($("#person_name").val()),
        person_id = $.trim($("#person_id").val()),
        input_file = $("#inputfile").val();
    let reg = /^[0-9]{8}$/;
    
    if (input_file.length === 0 || person_name === '' || person_id === '') {
        alert('你还有未填写的参数');
        return ;
    }else if (!reg.test(person_id)) {
        alert('请填写8位数字的ID');
        return ;
    }

    $.ajax({
        url:"/face_input",
        type: "POST",
        data: form_data,
        async: true,
        cashe: false,
        contentType:false,
        processData:false, //不希望将文件转化成ajax相应的对象，因此设为false。
        beforeSend:function(XMLHttpRequest){
            ajax_loading()
        }, 
        success:function (returndata) {
            if(returndata === 'ok'){
                ajax_ok();
                successful_operation();
                $("#uploadForm")[0].reset();
                // $.post('/restart_face',data = {"status":"restart"},function(result){
                //     if (result == 'ok') {
                //         alert('操作成功');
                //     }else{
                //         alert('操作失败');
                //     }
                // })
            }else{
                ajax_ok();
                alert(returndata);
            }
    　　}, 
    　　error: function (returndata) { 
    　　　　　alert("上传失败！")
        }
    })
})

//在type为file的input上面添加这个onchenge事件方法名为PreviewImage(this)
function PreviewImage(imgFile) 
{ 
    //使用这个方法来临时创建一个文件的链接，参数是一个file或者blob
    var path = URL.createObjectURL(imgFile.files[0]);
    //将链接赋值给上面的图片src路径
    $("#face_preview").prop("src",path);
    $("#preview_div").css({'border':'1px dotted orange'})
    $("#preview_div").css('padding','5px');
    //销毁上面创建的链接
    //URL.revokeObjectURL(path);
 }
 
$("#inputfile").change(function(e){
    PreviewImage(this)
})

let img_operateFormatter = function (value, row, index) {//赋予的参数
    return [
        '<button id="img_btn" class="btn btn-success" type="button">查看</button>',
    ].join('');
}

window.operateEvents = {
    "click #img_btn":function(e,value,row,index){
        let all_data = $("#face_table").bootstrapTable('getData',useCurrentPage=true);
        let img_list = new Array()
        for(let i = 0; i < all_data.length; i++){
            img_list.push(all_data[i]['img_url'])
        }
        // log(row)
        
        $.pictureViewer({
            images: img_list, //需要查看的图片，数据类型为数组
            initImageIndex: index + 1, //初始查看第几张图片，默认1
        });

    }
}

let TableInit = function(){
    let oTableInit = new Object();
    oTableInit.Init = function(){
        $("#face_table").bootstrapTable({
            url:'/get_face',
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
                field:'person_name',
                title:'姓名'
            },{ 
                field:'person_id',
                title:'个人id'
            },{
                field:'img_url',
                title:'图片',
                formatter:img_operateFormatter,
                events: operateEvents
            }]
        });
    };
    return oTableInit;
}

