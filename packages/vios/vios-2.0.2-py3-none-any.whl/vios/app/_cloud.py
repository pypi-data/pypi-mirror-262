import re
import time

import numpy as np
import requests

from vios.app import connect


server_url = '124.70.54.59/qbackend'  # cloud['server']
# cloud['token']
api_token = 'oQTjRK90iTrM0dit12ozHIZyy64wnqkm644ekuXpNN4.QfyczM2AzMzEzNxojIwhXZiwyM2AjM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye'


def openqasm_to_qlisp(openqasm: str, QMAP: dict = {}, verbose=True):
    if verbose:
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"""{'='*80}\r\n|{t}{' '*10}{'Transform circuit to qlisp'.ljust(68 -
              len(t))} {openqasm.count('measure')}|\r\n{'='*80}""")
    # if openqasm.count('measure') > 0:
    #     print(openqasm)

    lines = openqasm.split(';')

    qlisp = []
    read_qubits = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue

        operations_qbs = line.split(" ")
        operations = operations_qbs[0]
        if operations == "qreg":
            qbs = operations_qbs[1]
            num = int(re.findall("\d+", qbs)[0])
        elif operations == "creg":
            pass
        elif operations == "measure":
            mb = int(re.findall("\d+", operations_qbs[1])[0])
            cb = int(re.findall("\d+", operations_qbs[3])[0])
            qlisp.append((("Measure", cb), QMAP[mb]))
            read_qubits.append(QMAP[mb])
        else:
            qbs = operations_qbs[1]
            indstr = re.findall("\d+", qbs)
            inds = [int(indst) for indst in indstr]
            if operations == "barrier":
                qlisp.append(("Barrier", tuple([QMAP[i] for i in inds])))
            else:
                sp_op = operations.split("(")
                gatename = sp_op[0]
                if len(sp_op) > 1:
                    paras = sp_op[1].strip("()")
                    parastr = paras.split(",")
                    # paras = [eval(parai, {"pi":pi}) for parai in parastr]
                    paras = []
                    for parai in parastr:
                        if parai.endswith('us'):
                            paras.append(eval(parai.removesuffix('us'))*1e-6)
                        else:
                            paras.append(eval(parai, {"pi": np.pi}))

                if gatename == "cx":
                    qlisp.append(("Cnot", (QMAP[inds[0]], QMAP[inds[1]])))
                elif gatename == 'delay':
                    qlisp.append((('Delay', *paras), QMAP[inds[0]]))
                elif gatename == "cz":
                    qlisp.append(("CZ", (QMAP[inds[0]], QMAP[inds[1]])))
                elif gatename == "rx":
                    qlisp.append((("Rx", *paras), QMAP[inds[0]]))
                elif gatename == "ry":
                    qlisp.append((("Ry", *paras), QMAP[inds[0]]))
                elif gatename == "rz":
                    qlisp.append((("Rz", *paras), QMAP[inds[0]]))
                elif gatename in ("xyzh"):
                    qlisp.append((gatename.upper(), QMAP[inds[0]]))
                elif gatename in ["u1", "u2", "u3"]:
                    qlisp.append(((gatename, *paras), QMAP[inds[0]]))

    return qlisp, read_qubits


def clear(tid):
    result, task_status = {}, 'Failed'
    if task_status == 'Failed':
        #     print('failed')
        post_data = {
            "task_id": tid,
            "status": 'failed',
            "raw": "",
            "res": "",
            "server": 2,
        }

    try:
        res = requests.post(
            url=f"http://{server_url}/scq_result/",
            data=post_data,
            headers={'api_token': api_token})
        # proxies=proxies)
        print(res.text)
    except:
        print('POST ERROR')


def task_request(request_time=1, tid=0):

    qp = connect('QuarkProxy', port=3088)

    while True:
        res = None
        while res == None:
            time.sleep(float(request_time))
            try:
                res = requests.get(
                    url=f"http://{server_url}/scq_task_p50/",
                    timeout=10.0,
                    headers={'api_token': api_token}).json()
                # proxies=proxies
                print(time.strftime('%Y-%m-%d %H:%M:%S') +
                      '---requesting success', end='\r')
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S') + '---connecting loss')
                time.sleep(2.0)
                print('reconnecting...')

        task_id = str(res['task_id'])
        if task_id == tid:
            time.sleep(0.2)
            continue
        tid = task_id
        shots = int(res['shots'])
        circuit = str(res['circuit'])
        QMAP = eval(res['qubit_mapping'])

        try:
            circuit_qLisp, read_qubits = openqasm_to_qlisp(circuit, QMAP)

            task = {'chip': '#8',
                    'name': 'MyJob',
                    'tid': tid,
                    'token': api_token,
                    'circuit': circuit_qLisp,
                    'shots': shots}
            qp.run(task)
        except Exception as e:
            print(circuit, ">"*10, e)
            result, task_status = {}, 'Failed'
            clear(tid=tid)


if __name__ == '__main__':
    task_request(request_time=0.3, tid=0)
