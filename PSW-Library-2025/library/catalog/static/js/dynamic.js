function setOnMaintenance (id)
{
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function()
    {
       obj = JSON.parse(this.responseText);
       document.getElementById("span-" + id).innerHTML = obj.new_button;
       document.getElementById("para-" + id).innerHTML = obj.new_status;
       document.getElementById("para-" + id).className = obj.new_style;
    };
  xhttp.open("GET", "/catalog/set_book_on_maintenance/" + id);
  xhttp.send();
}

