"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from FlaskWebProject2 import app
import math
from math import sqrt
import matplotlib.pyplot as plt, mpld3
import numpy as np
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/drive')
def drive_page():
    return render_template('drive.html')

@app.route('/calculates')
def calculates_page():
    return render_template('calculates.html')

@app.route('/fan', methods=['GET', 'POST'])
def do_search()->str:
    power = request.form['power']
    voltnom = request.form['voltnom']
    speed = request.form['speed']
    speed2 = request.form['speed2']

    mot = 9.55
    z = int(voltnom) / pow(50, 2)
    polusa = 1

    try:
        int(power);
    except ValueError:
        power = 0;
    try:
        int(speed);
    except ValueError:
        speed = 0;
    try:
        int(speed2);
    except ValueError:
        speed2 = 0;

    if int(speed) > 400 and int(speed) <= 500:
        polus = 6
    if int(speed) > 500 and int(speed) <= 600:
        polus = 5
    if int(speed) <= 750 and int(speed)> 600:
        polusa = 4
    if int(speed) <= 1000 and int(speed) > 750:
        polusa = 3
    elif int(speed) > 900 and int(speed) < 2000:
        polusa = 2
    elif int(speed) > 2000:
        polusa = 1

    speed2_radian = (2 * 3.14 * int(speed2)) / 60
    speed2_Hz = (mot * speed2_radian * polusa) / 60
    z1 = z * speed2_Hz**2
    try:
        moment = (mot * (int(power) * 1000)) / int(speed)
    except ZeroDivisionError:
        moment = 0;
    try:
        s = int(voltnom) / z1
    except (ValueError, ZeroDivisionError):
        s = 0;
    try:
        moment2 = moment / s
    except ZeroDivisionError:
        moment2 = 0;

    #z2 = z1 * 1.73
    power2 = (moment2 * speed2_radian) / 1000
    moment2 = math.ceil(moment2)
    z1 = math.ceil(z1)
    speed2_Hz = math.ceil(speed2_Hz)
    power2 = math.ceil(power2)
    return render_template('results.html', the_power = str(power2), the_moment = str(moment2),
    the_volt = str(z1), the_speed2 = str(speed2_Hz), power_nom = str(power), speed_nom = str(speed), speed2_nom = str(speed2))

@app.route('/entry', methods=['GET', 'POST'])
def entry_page()-> 'html':
    return render_template('entry.html')

@app.route('/voltaa', methods=['GET', 'POST'])
def volta()-> 'html':
    sel1 = request.form.get('sel')
    vfd = request.form['vfd']
    cable_lenght = request.form['cable_lenght']
    voltage_nom = request.form['voltage_nom']
    current_nom = request.form['current_nom']

    try:
        float(sel1)
    except ValueError:
        sel1 = 0
    try:
        float(vfd)
    except ValueError:
        vfd = 0
    try:
        float(cable_lenght)
    except ValueError:
        cable_lenght = 0
    try:
        float(voltage_nom)
    except ValueError:
        voltage_nom = 0
    try:
        float(current_nom)
    except ValueError:
        current_nom = 0

    lenght_km = int(cable_lenght) / 1000
    vfd1 = (100 - int(vfd)) / 100

    cu = {'1.5':14.5, '2.5':8.87, '6':3.69, '10':2.19, '16':1.38, '25':0.87,
      '35':0.63, '50':0.47, '70':0.32, '95':0.23, '120':0.19, '150':0.15,
      '185':0.12, '240':0.097, '300':0.081}

    line = float(lenght_km) * float(cu[str(sel1)])
    z = round(line, 4)
    u_phase = float(current_nom) * z
    u_phase1 = (u_phase / 230) * 100
    u_phase2 = (100 - u_phase1) / 100
    u_mot = float(voltage_nom) * float(vfd1) * u_phase2
    return render_template('voltres.html', vfd = str(vfd), voltage_nom = str(voltage_nom), current_nom = str(current_nom), the_sel1 = str(sel1), z = str(z), u_phase = str(round(u_phase, 2)),
    u_phase1 = str(round(u_phase1, 2)), u_mot = str(round(u_mot, 2)))

@app.route('/voltagesag', methods=['GET', 'POST'])
def voltagesag()-> 'html':
    return render_template('voltagesag.html')

@app.route('/reac', methods=['GET', 'POST'])
def capacitor()-> 'html':
    transformer = request.form['transformer']
    customer_power = request.form['customer_power']
    cos_customer = request.form['cos_customer']
    cos = request.form['cos']
    volt_nom = request.form['volt_nom']
    cable_lenght = request.form['cable_lenght']
    m1 = request.form.get('m')
    cross_cable = request.form.get('cross_cable')

    try:
        int(transformer)
    except ValueError:
        transformer = 0

    try:
        float(customer_power)
    except ValueError:
        customer_power = 0

    try:
        float(cos_customer)
    except ValueError:
        cos_customer = 0

    try:
        float(cos)
    except ValueError:
        cos = 0

    try:
        int(volt_nom)
    except ValueError:
        volt_nom = 0

    try:
        int(cable_lenght)
    except ValueError:
        cable_lenght = 0

    try:
        int(cross_cable)
    except ValueError:
        cross_cable = 0

    cos_tan = {'0.8':0.75, '0.86':0.59, '0.9':0.48, '0.91':0.46, '0.92':0.43, '0.93':0.4,
               '0.94':0.36, '0.95':0.33, '0.96':0.29, '0.97':0.25, '0.98':0.2, '0.99':0.14, '1':0}

    alum = {'16':2.3, '25':1.4, '35':1, '50':0.77, '70':0.53, '95':0.39, '120':0.31,
          '150':0.25, '185':0.2, '240':0.15, '300':0.13}

    cupp = {'1.5':14.5, '2.5':8.87, '6':3.69, '10':2.19, '16':1.38, '25':0.87, '35':0.63, '50':0.47,
          '70':0.32, '95':0.23, '120':0.19, '150':0.15, '185':0.12, '240':0.097, '300':0.081}
    
    try:
        s_cus = float(customer_power) / float(cos_customer)#находим полную мощность потребителя
    except ZeroDivisionError:
        s_cus = 0
    try:
        q_cus = sqrt(pow(float(s_cus), 2) - pow(float(customer_power), 2))#находим реактив потребителя
    except ZeroDivisionError:
        q_cus = 0
    try:
        cb_current = float(customer_power) * 1000 /(1.73 * int(volt_nom) * float(cos_customer))#ток через автомат
    except ZeroDivisionError:
        cb_current = 0

    cable = int(cable_lenght) / 1000

    if str(m1) == "медный":
         r = float(cupp[str(cross_cable)]) * cable#берем сопротивление кабеля по сечению
    if str(m1) == "алюминиевый":
         r = float(alum[str(cross_cable)]) * cable#берем сопротивление кабеля по сечению

    cable_losses = (pow(cb_current, 2) * r) / 1000#джоулевы потери в кабеле
    try:
        tan = q_cus / float(customer_power)#находим тангенс по нужному косинусу
    except ZeroDivisionError:
        tan = 0

    qc = float(customer_power) * (tan - float(cos_tan[str(cos)]))#мощность батареи

    try:
        s_komp = float(customer_power) / float(cos)#полная мощность потребителя после компенсации
    except ZeroDivisionError:
        s_komp = 0
    try:
        cb_current2 = float(customer_power) * 1000 /(1.73 * int(volt_nom) * float(cos))#ток через автомат после компенсации
    except ZeroDivisionError:
        cb_current2 = 0

    cable_losses2 = (pow(cb_current2, 2) * r) / 1000#джоулевы потери в кабеле после компенсации
    return render_template('reactive_result.html', the_transformer = str(transformer), the_customer_power = str(customer_power), the_cos = str(cos),
    the_volt_nom = str(volt_nom), the_m1 = str(m1), the_cable_lenght = str(cable_lenght), the_cross_cable = str(cross_cable),
    the_s_cus = str(round(s_cus, 2)), the_q_cus = str(round(q_cus, 2)), the_cb_current = str(round(cb_current, 2)), the_r = str(round(r, 4)), the_cable_losses = str(round(cable_losses, 2)),
    the_qc = str(round(qc, 2)), the_cb_current2 = str(round(cb_current2, 2)), the_s_komp = str(round(s_komp, 2)), the_cable_losses2 = str(round(cable_losses2, 2)), the_cos_customer = str(cos_customer))

@app.route('/reactive', methods=['GET', 'POST'])
def reactive_page()-> 'html':
    return render_template('reactive.html')

@app.route('/sc', methods=['GET', 'POST'])
def shortcirc_page()-> 'html':
    system_power = request.form['system_power']#мощность системы
    trans_power = request.form['trans_power']#мощность трансформатора
    uk = request.form['uk']#напряжение короткого замыкания
    group = request.form.get('group')#группа соединения обмоток
    voltage = request.form['voltage']#номинальное напряжение на вторичной обмотке
    m = request.form.get('m')#от трансформатора шины или кабель
    l = request.form['l']#длина шин/кабеля в метрах
    cross = request.form.get('cross')#сечение шин
    cross2 = request.form.get('cross2')#сечение кабеля от трансформатора
    n = request.form.get('n')#сечение кабеля к потребителю
    cable_lenght = request.form['cable_lenght']#длина кабеля до потребителя
    cross_cable = request.form.get('cross_cable')#сечение кабеля

    try:
        int(system_power)
    except ValueError:
        system_power = 0
    try:
        int(trans_power)
    except ValueError:
        trans_power = 0
    try:
        float(uk)
    except ValueError:
        uk = 0
    try:
        float(voltage)
    except ValueError:
        voltage = 0
    try:
        int(cable_lenght)
    except ValueError:
        cable_lenght = 0

    cos_tan = {'0.8':0.75, '0.86':0.59, '0.9':0.48, '0.91':0.46, '0.92':0.43, '0.93':0.4,
        '0.94':0.36, '0.95':0.33, '0.96':0.29, '0.97':0.25, '0.98':0.2, '0.99':0.14, '1':0}

    al = {'16':2.3, '25':1.4, '35':1, '50':0.77, '70':0.53, '95':0.39,
        '120':0.31, '150':0.25, '185':0.2, '240':0.15, '300':0.13}

    cu = {'1.5':14.5, '2.5':8.87, '6':3.69, '10':2.19, '16':1.38, '25':0.87,
        '35':0.63, '50':0.47, '70':0.32, '95':0.23, '120':0.19, '150':0.15,
        '185':0.12, '240':0.097, '300':0.081}

    bus_al = {'25x3':0.475, '30x3':0.394, '30x4':0.296, '40x4':0.222, '40x5':0.177, '50x5':0.142,
        '50x6':0.118, '60x6':0.099, '60x8':0.074, '80x8':0.055, '80x10':0.0445, '100x10':0.0355,
        '2(60x8)':0.037, '2(80x8)':0.0277, '2(80x10)':0.0222, '2(100x10)':0.0178}

    bus_cu = {'25x3':0.268, '30x3':0.223, '30x4':0.167, '40x4':0.125, '40x5':0.1, '50x5':0.08,
        '50x6':0.067, '60x6':0.0558, '60x8':0.0418, '80x8':0.0313, '80x10':0.025, '100x10':0.02,
        '2(60x8)':0.0209, '2(80x8)':0.0157, '2(80x10)':0.0125, '2(100x10)':0.01}

    cable = int(cable_lenght) / 1000
    l1 = int(l) / 1000
    if str(m) == "Шины_медные":
        line = float(bus_cu[str(cross)]) * l1

    if str(m) == "Шины_алюминиевые":
        line = float(bus_al[str(cross)]) * l1

    if str(m) == "Кабель_медный":
        line = float(cu[str(cross2)]) * l1

    if str(m) == "Кабель_алюминиевый":
        line = float(al[str(cross2)]) * l1

    if str(n) == "Алюминиевый":
        r = float(al[str(cross_cable)]) * cable

    if str(n) == "Медный":
        r = float(cu[str(cross_cable)]) * cable

    try:
        xc = (float(voltage)**2) / int(system_power)
    except ZeroDivisionError:
        xc = 0
    try:
        xt = float(uk) * (float(voltage)**2) / ((float(trans_power)/1000) * 100)
    except ZeroDivisionError:
        xt = 0
    x1 = xc + xt
    x2 = xc + xt + line
    x3 = xc + xt + line + r
    try:
        k1_3 = float(voltage) / (1.73 * x1)
    except ZeroDivisionError:
        k1_3 = 0
    kud1 = k1_3 * 1.71
    k1_2 = 0.865 * k1_3
    k2_3 = float(voltage) / (1.73 * x2)
    kud2 = k2_3 * 1.71
    k2_2 = 0.865 * k2_3
    k3_3 = float(voltage) / (1.73 * x3)
    kud3 = k3_3 * 1.71
    k3_2 = 0.865 * k3_3
    k1_1 = 0
    k2_1 = 0
    k3_1 = 0
    if group == "D/Y":
        k1_1 = k1_3
        k2_1 = k2_3
        k3_1 = k3_3

    if group == "Y/Y":
        k1_1 = k1_3 / 2.5
        k2_1 = k2_3 / 2.5
        k3_1 = k3_3 / 2.5

    return render_template('shortresult.html', the_kud1 = str(round(kud1, 2)), the_k1_3 = str(round(k1_3, 2)), the_k1_2 = str(round(k1_2, 2)),
                           the_k1_1 = str(round(k1_1, 2)), the_kud2 = str(round(kud2, 2)), the_k2_3 = str(round(k2_3, 2)), the_k2_2 = str(round(k2_2, 2)),
                           the_k2_1 = str(round(k2_1, 2)), the_kud3 = str(round(kud3, 2)), the_k3_3 = str(round(k3_3, 2)), the_k3_2 = str(round(k3_2, 2)),
                           the_k3_1 = str(round(k3_1, 2)), the_system_power = str(system_power), the_trans_power = str(trans_power), the_uk = str(uk),
                           the_group = str(group), the_voltage = str(voltage), the_m = str(m), the_l = str(l), the_cross = str(cross), the_n = str(n),
                           the_cable_lenght = str(cable_lenght), the_cross_cable = str(cross_cable))

@app.route('/shortcircuit', methods=['GET', 'POST'])
def shortcircuit_page()-> 'html':
    return render_template('shotcircuit.html')

@app.route('/vhz', methods=['GET', 'POST'])
def volthertz()->str:
    mpower = request.form['mpower']
    voltage = request.form['voltage']
    speed = request.form['speed']   
    speed2 = request.form['speed2']

    try:
        int(mpower)
    except ValueError:
        mpower = 0
    try:
        int(voltage)
    except ValueError:
        voltage = 0
    try:
        int(speed)
    except ValueError:
        speed = 0
    try:
        int(speed2)
    except ValueError:
        speed2 = 0

    f = 50

    z = int(voltage) / f
    if int(speed) > 400 and int(speed) <= 500:
        polus = 6
    if int(speed) > 500 and int(speed) <= 600:
        polus = 5
    if int(speed) > 600 and int(speed) <= 750:
        polus = 4
    if int(speed) > 750 and int(speed) <= 1000:
        polus = 3
    if int(speed) > 1000 and int(speed) <= 1500:
        polus = 2
    if int(speed) > 1500 and int(speed) >= 3000:
        polus = 1

    w_nom = (2 * 3.14 * int(speed)) / 60#скорость в радианах
    w_2 = (2 * 3.14 * int(speed2)) / 60#требуемая скорость в радианах
    f2 = (9.55 * w_2 * polus) / 60#тебуемая скорость в герцах
    u2 = z * f2#напряжение на статоре
    m_nom = (9.55 * int(mpower) * 1000) / int(speed)#номинальный момент
    power2 = (m_nom * int(speed2) / 9.55)#потребляемая мощность при требуемой скорости
    m_2 = (9.55 * power2) / int(speed2)
    power3 = power2 / 1000#потребляемая мощность в кВт
    return render_template('volthzres.html', the_mpower = int(mpower), the_voltage = int(voltage), the_f = int(f),
                           the_speed = int(speed), the_speed2 = int(speed2), the_power3 = float(round(power3, 2)),
                           the_m_2 = float(round(m_2, 2)), the_u2 = float(round(u2, 2)), the_f2 = float(round(f2, 2)))

@app.route('/volthz', methods=['GET', 'POST'])
def volthz_page()-> 'html':
    return render_template('volthz.html')

@app.route('/volthzres', methods=['GET', 'POST'])
def volthzres_page()-> 'html':
    return render_template('volthzres.html')

@app.route('/admeh', methods=['GET', 'POST'])
def admeh_page()-> 'html':
    return render_template('admeh.html')

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    syncspeed = request.form['syncspeed']
    nomspeed = request.form['nomspeed']
    power = request.form['power']
    Kmoment = request.form['Kmoment']

    snom = (int(syncspeed) - int(nomspeed)) / int(syncspeed)
    moment = (9.55 * int(power) * 1000) / int(syncspeed)
    momentkr = float(Kmoment) * moment

    x = []; y = []; s = 0

    plt.title('Механическая характеристика асинхронного двигателя', fontsize=12) #заголовок
    plt.xlabel('Скольжение', fontsize=10) # ось абсцисс
    plt.ylabel('Момент', fontsize=10) # ось ординат
    plt.grid()

    while s <= 1:
        skr = snom * (float(Kmoment) + math.sqrt(pow(float(Kmoment), 2) - 1))
        try:
            s1 = s / skr
        except ZeroDivisionError:
            s1 = 0
        try:
            s2 = skr / s
        except ZeroDivisionError:
            s2 = 0
        try:
            mkr = (float(momentkr) * 2) / (s1 + s2)
        except ZeroDivisionError:
            mkr = 0
        x.append(s)
        y.append(mkr)
        s += 0.008
        plt.plot(x, y, 'r', linewidth=1) # построение графика)

    return mpld3.show()

    return render_template('mehres.html')
