function toggle(id) {
    let t = document.getElementById(id).checked;
    document.getElementById('tog'+id).value = t;
    // document.getElementById('card'+id).value = id
    document.getElementById('toggle'+id).submit();
}


function TDate(id) {
    var UserDate = document.getElementById('calendar'+id).value;
    var ToDate = new Date();
    console.log(UserDate)

    if (new Date(UserDate).getTime() < ToDate.getTime()) {
        alert("The Date must be Bigger or Equal to today date");
        return false;
    }
    return true;
}

function updateTime(lists) {
    for (let [list_id, datetime] of Object.entries(lists)) {
        let d = new Date(datetime).getTime();
        let p = new Date().getTime();
        let ms = parseInt((p-d)/(1000*60))
        let time = 'mins'
        if (ms > 60) {
            ms = parseInt(ms/60)
            time = 'hours'
            if (ms > 24) {
                ms = parseInt(ms/24)
                time = 'days'
            }
        }
        if (ms<=1) {
            time = time.replace("s","")
        }
        document.getElementById('update_time'+list_id).innerHTML = 'Last updated '+ms+' '+time+' ago';
    }
}

function updateColorN(cards) {
    for (let [card_id, deadline] of Object.entries(cards)) {
        let dt = new Date(deadline).getTime()
        let td = new Date().getTime();
        let diff = parseInt((dt-td)/(1000*60*60))
        if (0<diff && diff<24) {
            document.getElementById('font_color'+card_id).style.color = 'orange';
        }
        if (diff <= 0 ) {
            document.getElementById('font_color'+card_id).style.color = 'red'
        }
    }
}

function updateColorY(cards) {
    for (let [card_id, [deadline, complete_date]] of Object.entries(cards)) {
        let dt = new Date(deadline).getTime()
        let cd = new Date(complete_date).getTime()
        let diff = dt-cd
        if (diff <= 0) {
            document.getElementById('font_color'+card_id).style.color = 'red'
        }
    }
}