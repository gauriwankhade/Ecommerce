//sidenav
var elem = document.querySelector('.sidenav');
var instance1 = new M.Sidenav(elem,{});
      
          
var elem4 = document.querySelector('.dropdown-trigger');
var instance4 = new M.Dropdown(elem4);


var elem2 = document.querySelector('.tabs');
        var instance2 = new M.Tabs(elem2);

        function myFunction() {
          var url = "{% url 'login_url' %}"; 
 
          window.open(url); 
   		} 
