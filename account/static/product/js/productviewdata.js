$(document).ready(function(){


    $("#first_date").change(function(){

   
        date_toggle = 1;
        $("#page-p").click();
    
        
    });
    
    
    $("#last_date").change(function(){
    
        
        date_toggle = 1;
        $("#page-p").click();
    
        
    });    

first_html='<li class="page-item"><a class="page-link" id="page-p" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
$("#main-pag-nation").append(first_html);
    

date_toggle = 0;

last_page = '1'

$('#main-pag-nation').on('click','.page-link',function(){
csrftoken = Cookies.get('csrftoken');

var page_id = ($(this)[0].id).split("-");
if(date_toggle == 0){

        page_id = page_id[1];
        console.log(page_id);
        if(page_id == 'n'){
            console.log('n');
            
            page_id = (parseInt(last_page) + 1).toString();
            max_val = $("#page-shift-max")[0].value;
            if(parseInt(page_id)>parseInt(max_val)){
                page_id = max_val

            }
        }
        else if(page_id == 'p'){
            console.log('p');

            page_id = (parseInt(last_page) - 1).toString();
            
            if(page_id == '0'){
                page_id='1';
            }

        }

}
else{

    page_id='1'

}
date_toggle = 0;
last_page = page_id

first_date = $("#first_date").val();
last_date = $("#last_date").val();

$.ajax({
    url: '/product/view/',
    type: 'POST',
    data: {'page_no':page_id,'first_date':first_date,'last_date':last_date},
    headers: { "X-CSRFToken": csrftoken },
    dataType: 'json',
    success: function(data) {

        
        var frag = (data.pages).toString();
       
        $("#page-shift-max")[0].value = frag;
        


        $("#view-table").empty();

        $("#main-pag-nation").empty();



        ar_data = data.final_data
        pages_no = data.pages
       
        data_len = ar_data.length

        first_html='<tr><th>Id</th><th>Sheet Count</th><th>Sheet Residue</th><th>Date</th><th>Created By</th><th>Created Date</th></tr>'
        $("#view-table").append(first_html);  
        for(var i=0;i<data_len;i++){

            first_html = "<tr><td>"+ ar_data[i][0] +"</td><td>"+ ar_data[i][1] +"</td><td>"+ ar_data[i][2] +"</td>"
            second_html = "<td>"+ ar_data[i][3] +"</td><td>"+ ar_data[i][4] +"</td><td>"+ ar_data[i][5] +"</td></tr>"
            full_html = first_html + second_html
            $("#view-table").append(full_html);

        }

        first_html='<li class="page-item"><a class="page-link" id="page-p" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        $("#main-pag-nation").append(first_html);


        second_html = '<li class="page-item"><a class="page-link" id="page-n" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        for(var i=0;i<pages_no;i++){

            first_html = "<li class='page-item'><a class='page-link' id='page-"+ (i+1).toString() +"' href='#'>"+ (i+1).toString() +"</a></li>";
            
            
            
            $("#main-pag-nation").append(first_html);
        }
        $("#main-pag-nation").append(second_html);

        

        
    }


 });

});





var dt = new Date();
var month = parseInt(dt.getMonth())
month = (month+1).toString();
if(month.length==1){
    month = "0"+month
}

dt= dt.getFullYear()+"-"+ month + "-" + dt.getDate();

$("#first_date").val("2021-04-01");
$("#last_date").val(dt);




$(".page-link").click();

})