let log = console.log

var face_chart = Highcharts.chart('face_container',{
    credits:{
        enabled:false
    },
    exporting: { 
        enabled: false 
    },
    chart: {
        type: 'column'
    },
    title: {
        text: '人脸识别统计'
    },
    xAxis: {
        // categories: [],
        crosshair: true,
        labels:{
            style:{
                fontSize:'16px'
            }
        }
    },
    yAxis: {
        allowDecimals:false,
        min: 0,
        title: {
            text: '数量'
        }
    },
    tooltip: {
        // head + 每个 point + footer 拼接成完整的 table
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            borderWidth: 0
        },
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }
    },
    series: [{
        name: '未知人员',
        data: []
    }, {
        name: '已授权',
        data: []
    }]
});

var intrusion_chart = Highcharts.chart('intrusion_container',{
    credits:{
        enabled:false
    },
    exporting: { 
        enabled: false 
    },
    chart: {
        type: 'column'
    },
    title: {
        text: '越界检测统计'
    },
    xAxis: {
        // categories: [],
        crosshair: true,
        labels:{
            style:{
                fontSize:'16px'
            }
        }
    },
    yAxis: {
        allowDecimals:false,
        min: 0,
        title: {
            text: '报警次数'
        }
    },
    tooltip: {
        // head + 每个 point + footer 拼接成完整的 table
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            borderWidth: 0
        },
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }
    },
    series: [{
        name: '越界报警次数',
        data: []
    }]
});

var safedress_chart = Highcharts.chart('safedress_container',{
    credits:{
        enabled:false
    },
    exporting: { 
        enabled: false 
    },
    chart: {
        type: 'column'
    },
    title: {
        text: '安全着装识别统计'
    },
    xAxis: {
        // categories: [],
        crosshair: true,
        labels:{
            style:{
                fontSize:'12px'
            }
        }
    },
    yAxis: {
        allowDecimals:false,
        min: 0,
        title: {
            text: '报警次数'
        }
    },
    tooltip: {
        // head + 每个 point + footer 拼接成完整的 table
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            borderWidth: 0
        },
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }
    },
    series: [{
        name: '安全帽报警',
        data: []
    },{
        name: '工作服报警',
        data: []
    }]
});

var panel_chart = Highcharts.chart('panel_container',{
    credits:{
        enabled:false
    },
    exporting: { 
        enabled: false 
    },
    chart: {
        type: 'column'
    },
    title: {
        text: '面板识别统计'
    },
    xAxis: {
        // categories: [],
        crosshair: true,
        labels:{
            style:{
                fontSize:'12px'
            }
        }
    },
    yAxis: {
        allowDecimals:false,
        min: 0,
        title: {
            text: '报警次数'
        }
    },
    tooltip: {
        // head + 每个 point + footer 拼接成完整的 table
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            borderWidth: 0
        },
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }
    },
    series: [{
        name: '报警次数',
        data: []
    }]
});

$("#intrusion_month").change(function(e){
    let month = $("#intrusion_month").val()
    let data = {
        "application":"intrusion",
        "month":month
    }
    $.post('/get_statistics',data = data, function(result){
        log(result)
        if(result){
            let camera = [],
                total = [];
            for(let i = 0; i < result.length; i++){
                tmp = result[i]['description'] + '(' + result[i]['camera_id'] + ')'
                camera.push(tmp)
                total.push(result[i]['total'])
            }
            
            intrusion_chart.xAxis[0].categories = camera
            intrusion_chart.update({
                series: [{
                type: 'column',
                name: '越界报警次数',
                data: total
                }]
            })
            intrusion_chart.redraw()  
        }else{
            alert('查询失败')
        }
    })
})

$("#panel_month").change(function(e){
    let month = $("#panel_month").val()
    let data = {
        "application":"panel",
        "month":month
    }
    $.post('/get_statistics',data = data, function(result){
        log(result)
        if(result){
            let camera = [],
                total = [];
            for(let i = 0; i < result.length; i++){
                tmp = result[i]['description'] + '(' + result[i]['camera_id'] + ')'
                camera.push(tmp)
                total.push(result[i]['total'])
            }
            
            panel_chart.xAxis[0].categories = camera
            panel_chart.update({
                series: [{
                type: 'column',
                name: '报警次数',
                data: total
                }]
            })
            panel_chart.redraw()  
        }else{
            alert('查询失败')
        }
    })
})

$("#face_month").change(function(e){
    let month = $("#face_month").val()

    let data = {
        "application":"face",
        "month":month
    }
    $.post('/get_statistics',data = data, function(result){
        log(result)
        if (result) {
            let camera = [],
                known_total = [],
                unknown_total = [];
            for(let i = 0; i < result.length; i++){
                camera_id = result[i]['description'] + '(' + result[i]['camera_id'] + ')'
                camera.push(camera_id)
                known_total.push(result[i]['alarm'][1]['total'])
                unknown_total.push(result[i]['alarm'][0]['total']) 
            }
            
            face_chart.xAxis[0].categories = camera
            face_chart.update({
                series: [{
                    type: 'column',
                    name: '未知人员',
                    data: unknown_total
                },{
                    type: 'column',
                    name: '已授权',
                    data: known_total 
                }]
            })
            face_chart.redraw()
        }else{
            alert('查询失败')
        }   
    })
})

$("#safedress_month").change(function(e){
    let month = $("#safedress_month").val()
    let data = {
        "application":"safedress",
        "month":month
    }
    $.post('/get_statistics',data = data, function(result){
        log(result)
        if(result){
            let camera = [],
                helmet_total = [],
                clothes_total = [];
            for(let i = 0; i < result.length; i++){
                camera_msg = result[i]['description'] + '(' + result[i]['camera_id'] + ')'
                camera.push(camera_msg)
                helmet_total.push(result[i]['alarm'][0]['total'])
                clothes_total.push(result[i]['alarm'][1]['total'])
            }
            
            safedress_chart.xAxis[0].categories = camera
            safedress_chart.update({
                series: [{
                    type: 'column',
                    name: '安全帽报警',
                    data: helmet_total
                },{
                    type: 'column',
                    name: '工作服报警',
                    data: clothes_total
                }]
            })
            safedress_chart.redraw()  
        }else{
            alert('查询失败')
        }
    })
})