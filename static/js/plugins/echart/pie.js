function pie(k,v){

    option = {
        title : {
            text: '',
            subtext: '',
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: [],
            formatter: function (name) {
                    for(i=0;i<v.data.length;i++){
                        if(name === v.data[i].name){
                            rt = name + "(" + v.data[i].value + ")"
                       }
                   }
                   return rt
            },
        },
        toolbox: {
            show : true,
            feature : {
                magicType : {
                    show: true, 
                },
            restore : {show: true},
            saveAsImage : {show: true}
        }
        },
        series : []
    };

    series_data = {'name': v.text,'type': v.type,'radius' : '60%','data' : v.data}
    option.title.text = v.text;
    option.title.subtext = v.subtext;
    option.legend.data = v.legend;
    option.series.push(series_data);
    var fms_type_chart = echarts.init(document.getElementById(k));
    fms_type_chart.setOption(option);
}
