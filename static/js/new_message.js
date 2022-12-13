
const domContainer = document.querySelector('#root');
const root = ReactDOM.createRoot(domContainer);

const box = (
    <div class='box'>
        <input class='inp' name='for' placeholder="Send to:" autocomplete='off'></input>
        <input class='inp' name='theme' placeholder="Theme:" autocomplete='off'></input>

        <div contenteditable='true' id='text' name='text' placeholder='Message:'></div>

        <button id='send' onClick={() => send()}>Send</button>

    </div>
);

root.render(box);


function send(){
    let to = document.querySelector("input[name='for']").value;
    let theme = document.querySelector("input[name='theme']").value;
    let message = document.getElementById('text').innerText.replaceAll("\n", '<br>');

    if (to.length == 0 || message.length == 0){
        show_push("Все поля должны быть заполнены");
        return;
    }

    while (to[to.length - 1] == " "){
        to = to.slice(0, -1);
    }

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let f = fetch(`/send?to=${to}&theme=${theme}&message=${message}`).then(function(resp){
        return resp.json()
    }).then(function(data){
        if (data.status != 'ok'){
            show_push(data.status);
            return;
        }

        show_push("Отправлено!");
        setTimeout(function(){
            window.history.go(-1);
        }, 3100);
    })
}
