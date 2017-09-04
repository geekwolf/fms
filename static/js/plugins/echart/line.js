function line(k,v){
    option = {
      title : {
        text: '未来一周气温变化',
        subtext: '纯属虚构'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['邮件营销','联盟广告']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : []
};
    if(v.text && v.subtext){
 	option.title.text = v.text;
	option.title.subtext = v.subtext;
    }
    option.legend.data = v.legend;
    option.xAxis[0].data = v.xaxis_data;
    option.series = v.data;
    var fms_type_chart = echarts.init(document.getElementById(k));
    fms_type_chart.setOption(option);
  }                  
