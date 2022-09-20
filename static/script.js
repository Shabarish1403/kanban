function toggle(id) {
    let t = document.getElementById(id).checked;
    document.getElementById('tog'+id).value = t;
    document.getElementById('card'+id).value = id
    document.getElementById('toggle'+id).submit();
}


function TDate() {
    var UserDate = document.getElementById("calendar").value;
    var ToDate = new Date();

    if (new Date(UserDate).getTime() < ToDate.getTime()) {
        alert("The Date must be Bigger or Equal to today date");
        return false;
    }
    return true;
}