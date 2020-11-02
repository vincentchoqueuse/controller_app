import json
import numpy as np
from tools import system
import sys
import warnings
warnings.filterwarnings("error")

def lambda_handler(event, context):
    
    origin ='*'
    
    try :
        data = json.loads(event["body"])
        name = data["name"]
        num=np.fromstring(data["sys_num"],sep=',')
        den=np.fromstring(data["sys_den"], sep=',')
        sys_type = data["sys_type"]
        CL = data["controller_Cl"]
        Ki = float(data["controller_Ki"])
        Ti = float(data["controller_Ti"])
        type = data["controller_type"]
        color = data["color"]
        plot_type = data["plot_type"]
        sys_type = data["sys_type"]
        
        if plot_type=="nichols":
            CL = False
            name = "{} (open loop)".format(name)
        
        if  sys_type == "discrete":
            Ts = float (data["sys_Ts"])
            tf = system(num,den,type,Ki,Ti,CL,Ts=Ts)
        else:
            tf = system(num,den,type,Ki,Ti,CL)
    
        #set marker / line color
        marker_dict = {"color":color}
        line_dict ={"color":color}
    
    
        if plot_type == "time":
            
            N = min(int(data["N"]),1000)
            t,s = tf.step(N=N)

            if  sys_type == "discrete":
                line_dict ={"color":color,"shape":"hv"}
                output = {"x": t.tolist(), "y": s.tolist(),"name":name,"mode":"lines","line":line_dict,"marker":marker_dict}
            else:
                
                output = {"x": t.tolist(), "y": s.tolist(),"name":name,"mode":"lines","line":line_dict,"marker":marker_dict}
        
        if plot_type == "bode":
            
            n = min(int(data["n"]),1000)
            w, mag, phase = tf.bode(w=None,n=n)
            mag = 20*np.log10(mag)
            output = [{"x": w.tolist(), "y": mag.tolist(), "yaxis": 'y1',"name":"{} (mag)".format(name),"line":line_dict,"marker":marker_dict},
                    {"x": w.tolist(), "y": phase.tolist(),"yaxis": 'y2',"name":"{} (phase)".format(name),"line":line_dict,"marker":marker_dict}]
    
        if plot_type == "nichols":
            
            n = min(int(data["n"]),1000)
            w, mag, phase = tf.bode(w=None,n=n)
            mag = 20*np.log10(mag)
            hovertemplate = "<b>w</b>: %{text:.3f} rad/s<br><b>mag</b>: %{y:.3f} dB<br><b>phase</b>: %{x:.3f} deg<br>"
            output = {"x": phase.tolist(), "y": mag.tolist(),"name":name,"hovertemplate": hovertemplate, "text":w.tolist(),"line":line_dict,"marker":marker_dict}
        
        if plot_type == "zpmap":
            
            poles = tf.poles()
            zeros = tf.zeros()
            
            marker_dict_poles = {"color":color,"symbol":"x","size":12}
            marker_dict_zeros = {"color":color,"symbol":"circle-open","size":12,"line":{"width":2}}
            output = [
                    {"x": np.real(poles).tolist(), "y": np.imag(poles).tolist(),"name":"{} (poles)".format(name),"mode":"markers","marker":marker_dict_poles,"line":line_dict},
                    {"x": np.real(zeros).tolist(), "y": np.imag(zeros).tolist(),"name":"{} (zeros)".format(name),"mode":"markers","marker":marker_dict_zeros,"line":line_dict},
                    ]
        
        json_output  =  {'statusCode': 200,'body': json.dumps(output),'headers': {'Access-Control-Allow-Headers': 'Content-Type','Access-Control-Allow-Origin':origin,'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}}
    
    except Exception as error:
        json_output  = {'statusCode': 200,'body': json.dumps({"error":str(error)}),'headers': {'Access-Control-Allow-Headers': 'Content-Type','Access-Control-Allow-Origin': origin,'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}}

        #https://controlapp.s3-eu-west-1.amazonaws.com
    return json_output



