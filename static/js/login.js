
const domContainer = document.querySelector('#root');
const root = ReactDOM.createRoot(domContainer);

const title = <p>Log In</p>;
const login = <input class='inp' name='login' placeholder='Login:' autocomplete='off'></input>
const password = <input class='inp' id='password' name='password' placeholder='Password:' autocomplete='off' type='password'></input>;
const checkbox = <input type="checkbox" id='checkbox' onClick={()=>checkbox_clicked()}></input>;
const login_button = <button class='login' id='login_button' onClick={() => log_in()}>Login</button>

const box = (
    <div class='box'>
        {title}
        {login}
        {password}
        <div class='checkbox_box'>{checkbox} <p>Show password</p></div>
        {login_button}
        <a href='/signup'>SignUp</a>
    </div>
);

root.render(box);


function checkbox_clicked(){
    let box = document.querySelector('#checkbox');
    
    if (box.checked == true){
        document.querySelector("#password").type = 'text';
    }else{
        document.querySelector("#password").type = 'password';
    }
}

function log_in(){
    let login = document.querySelector('input[name="login"]').value;
    let password = document.querySelector('input[name="password"]').value;

    if (login.length == 0 || password.length == 0){
        show_push("Все поля долны быть заполнены");
        return;
    }

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/user_login?login=${login}&password=${password}`, {
        method: "GET",
        headers:{'X-CSRFToken': csrf},

    }).then((response) => {
        return response.json().then((data) => {
            if (data.status != 'ok'){
                show_push(data.status);
                return;
            }

            window.open("/", "_self");
        })
    });
}