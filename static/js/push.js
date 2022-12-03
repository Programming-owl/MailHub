const domContainer = document.querySelector('#push');
const root = ReactDOM.createRoot(domContainer);

const box = (
    <div class='push_box'><p id='push_text'>Неверный логин</p></div>
);

root.render(box);

function show_push(text){
    document.querySelector('#push_text').textContent = text;
    document.querySelector(".push_box").style.transform = 'translateY(0px)';

    setTimeout(function(){
        document.querySelector(".push_box").style.transform = 'translateY(-100px)';
    }, 3000);
}