function check_me(input_id){
    console.log(input_id)
    var checked_input = document.querySelector("input[id=cb_" + input_id + "]");
    var checked_label = document.querySelector("label[name=lb_" + input_id + "]");

    if (checked_input.checked){
        checked_label.style.textDecoration = "line-through";
    }
    else {
        checked_label.style.textDecoration = "";
    }
    var btn = document.getElementById("remove_btn");

    btn.value = "REMOVE ITEMS";
    btn.style.color = "#FFFFFF";
    btn.style.backgroundColor = "#FE7575";
    btn.style.cursor = "pointer";
}

function change_me(input_id, name){
    var changed_label = document.querySelector("label[name=lb_" + input_id + "]");
    url_data = [
        {"Value":document.getElementById(name + "_" + input_id).value},
        {"Name":input_id},
        {"name":name}
        ];
    console.log(url_data)
    changed_label.style.backgroundColor =  "#FFFF00";

    $.ajax({
    type: "POST",
    url: "/process_url",
    data: JSON.stringify(url_data),
    contentType: "application/json",
    dataType: 'json'
    });
}

function remove_me(input_string){
    console.log(input_string)
}