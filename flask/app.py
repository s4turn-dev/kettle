from flask import Flask, render_template, request
from turbo_flask import Turbo
import threading
import time
from kettle import MiMak1
from kettle.config import KETTLE_CAPACITY

app = Flask(__name__)
turbo = Turbo(app)

k = MiMak1()


def update_temperature():
    with app.app_context():
        while True:
            now_busy = k.isBusy
            time.sleep(1)
            if k.isBusy:
                k.boil()
                # Без этой заглушки раз в секунду обновляется только блок информации о чайнике, и в случае, когда чайник
                # завершает кипячение самостоятельно, текст кнопки кипячение не изменяется
                if now_busy != k.isBusy:
                    turbo.push(turbo.replace(render_template('command_panel.html'), 'command_panel'))
            else:
                k.cool()
            turbo.push(turbo.replace(render_template('state_table.html'), 'state_table'))


with app.app_context():
    threading.Thread(target=update_temperature).start()


@app.get('/')
def index():
    return render_template('kettle.html')


@app.post('/')
def change_kettle_state():
    action = request.form.to_dict()
    match list(action.keys())[0]:
        case 'power':
            k.switch_power()
        case 'busy':
            k.switch_busy()
        case 'inserted_amount':
            inserted_amount = action.get('inserted_amount')
            k.add_water(float(inserted_amount) if inserted_amount else 0)

    return turbo.stream([
        turbo.replace(render_template('state_table.html'), 'state_table'),
        turbo.replace(render_template('command_panel.html'), 'command_panel'),
    ])


@app.context_processor
def get_kettle_state():
    return {
        'isPowered': {
            'status': 'Да' if k.isPowered else 'Нет',
            'action': 'ОТКЛЮЧИТЬ' if k.isPowered else 'ВКЛЮЧИТЬ',
        },
        'isBusy': {
            'status': 'Да' if k.isBusy else 'Нет',
            'action': 'ОСТАНОВИТЬ' if k.isBusy else 'НАЧАТЬ',
        },
        'water_amount': k.water_amount,
        'capacity': KETTLE_CAPACITY,
        'temperature': 'вода не обнаружена' if k.is_empty() else f'{k.current_temperature}°С',
    }
