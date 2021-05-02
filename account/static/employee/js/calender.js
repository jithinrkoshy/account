$(document).ready(function(){

    month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']


    yr_list = []

   

   for(var i=0;i<$("#cal-year")[0].length;i++){

  
    yr_list.push($("#cal-year")[0][i].value);

   }


   

    $('#submit-calender').click(function(e){

            e.preventDefault();
            start_day_index = {'Sun':1,'Mon':2,'Tue':3,'Wed':4,'Thu':5,'Fri':6,'Sat':7}
            csrftoken = Cookies.get('csrftoken');
            
            var cal_month = $("#cal-month");
            var cal_year = $("#cal-year");
        
            var selected_date = cal_year[0].value.toString() + "-" + cal_month[0].value.toString();


          
             
            $.ajax({
                url: '/employee/calender',
                type: 'POST',
                data: {'date':selected_date,},
                headers: { "X-CSRFToken": csrftoken },
                dataType: 'json',
                success: function(data) {
                       
                    
                        for(var i=1;i<36;i++){

                            c_name = "c-" + i.toString();
                            $("."+c_name).html("")
                                

                        }

                        var days = data.days;
                        var log_flag = data.log_flag;
                        

                        var start_day = start_day_index[data.start_day];
                        var x = start_day
                        var index = start_day
                        
                        for(var i=0;i<days.length;i++){

                            x = index%35;
                            index++;
                            if(x==0){
                                x=35;
                            }
                            c_name = "c-" + x.toString();
                            if(log_flag[i]==0){
                                day_value = "<span class='red'>" + days[i].toString() + "</span>";
                            }    
                            else if(log_flag[i]==1){
                                day_value = "<span class='green'>" + days[i].toString() + "</span>";
                            }
                            else if(log_flag[i]==2){
                                day_value = "<span class='purple'>" + days[i].toString() + "</span>";
                            }
                            else if(log_flag[i]==3){
                                day_value = "<span class='chartreuse'>" + days[i].toString() + "</span>";
                            }
                            else if(log_flag[i]==4){
                                day_value = "<span class='green'>" + days[i].toString() + "</span><div class='cal-warning'></div>";
                            }     
                            else if(log_flag[i]==-1){
                                day_value = "<span class='black'>" + days[i].toString() + "</span>";
                            }           
                            $("."+c_name).html(day_value);

                        }




                }
           
           
             });

    });

    //Refreshing calender with current date
    var d = new Date()

    

    today_month = (d.getMonth()+1).toString()
    if(today_month.length==1){
        today_month = "0" + today_month;
    }
    $('#cal-month').val(today_month);

    

    $('#cal-year').val((d.getFullYear()).toString());

    $('#submit-calender').click();

    $("#cal-month").change(function(){
        $('#submit-calender').click();

    });
    $("#cal-year").change(function(){
        $('#submit-calender').click();

    });


    //Refreshing calender with current date

    //Calender next and prev

    $("#btn-prev").click(function(){

       var m_inp =  $('#cal-month').val();
       var y_inp =  $('#cal-year').val();
       var lm_index = month_list.indexOf(m_inp);
       var ly_index = yr_list.indexOf(y_inp);

       if(m_inp == "01"){

        ly_index--
        if(ly_index<0){

            ly_index = yr_list.length -1
            $('#cal-year').val(yr_list[ly_index]);
            


        }
        else{

            $('#cal-year').val(yr_list[ly_index]);
        }

        lm_index = month_list.length -1
        $('#cal-month').val(month_list[lm_index]);

       }
       else{
        lm_index--;
       
        $('#cal-month').val(month_list[lm_index]);
       }
 
       $('#submit-calender').click();
    });


    $("#btn-next").click(function(){

        var m_inp =  $('#cal-month').val();
        var y_inp =  $('#cal-year').val();
        var lm_index = month_list.indexOf(m_inp);
        var ly_index = yr_list.indexOf(y_inp);
 
        if(m_inp == "12"){
 
         ly_index++
         if(ly_index>yr_list.length -1){
 
             ly_index = 0
             $('#cal-year').val(yr_list[ly_index]);
             
 
 
         }
         else{
 
             $('#cal-year').val(yr_list[ly_index]);
         }
 
         lm_index = 0
         $('#cal-month').val(month_list[lm_index]);
 
        }
        else{
         lm_index++;
        
         $('#cal-month').val(month_list[lm_index]);
        }
  

        $('#submit-calender').click();
     });


    //Calender next and prev


    

})