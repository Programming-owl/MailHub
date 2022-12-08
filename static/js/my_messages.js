
const domContainer = document.querySelector('#root');
const root1 = ReactDOM.createRoot(domContainer);

const header = (
    <div class='header'>
        <div class='user_icon_div' onClick = {() => user_icon_click()}>
            <img src='/static/user.png' id='user_icon'></img>
        </div>

        <img src='/static/owl.png' class='owl'/>

        <div class='user_options' id='user_options'>

            <div id='sent' onClick={() => window.open('/sent', "_self")}>
                <img src='static/sent-mail.png'/>
                <p>Отправленно</p>
            </div>

            <div id='received' onClick={() => window.open("/", "_self")}>
                <img src='static/received.png'/>
                <p>Входящие</p>
            </div>

            <div id='logout' onClick={() => window.open("/logout", "_self")}>
                <img src='static/logout.png'/>
                <p>Выйти</p>
            </div>
        </div>
    </div>
);

function show_messages(){
    let f = fetch("/get_sent").then(function(resp){
        return resp.json();
    }).then(function(data){

        if (data.ans == 'None' || data.ans.length == 0){
            b = <h2>None</h2>;
            return rend(b)
        }

        var i;
        
        let box = [];

        for (i in data.ans){
            
            let elem = data.ans[i]
            let from;

            from = <p id='from'>To:&nbsp;&nbsp;{elem.to}  | </p>


            let block = (
                <div class='message' id={elem.id} onClick={()=>window.open(`/message/${elem.id}`, "_self")}>
                    
                    <div id='from_div'>
                        {from}

                        <p id='theme'>{elem.theme}</p>
                        <p id='message_text'>- {elem.message}</p>
                    </div>
                </div>
            );

            box.push(block);
        }

        let b = (
            <div class='messages_box'>
                <div id='padding'><p>Отправленно</p></div>
                {box}
                <div id='padding2'></div>
            </div>
        );

        console.log(b);

        return rend(b)
    });
}


const button = (
    <button id='add' onClick={() => window.open("/new_message", "_self")}><img src='/static/sent-mail.png'/></button>
);

const start_ico = <img src='/static/owl.png' class='start_ico'/>

root1.render(start_ico);

function rend(b){
    root1.render([header, (b), button]);
}


show_messages();

let lamp1 = 0;

function user_icon_click(){
    if (lamp1 == 0){
        document.querySelector("#user_options").style.display = 'flex';
        lamp1 = 1;
    } else if (lamp1 == 1){
        document.querySelector("#user_options").style.display = 'none';
        lamp1 = 0;
    }
}