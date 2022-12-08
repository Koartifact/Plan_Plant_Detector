import json
import glob


def convert(size, box):
        dw = 1./size[0]
        dh = 1./size[1]
        x = (box[0] + box[1])/2.0
        y = (box[2] + box[3])/2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = round(x*dw, 6)
        w = round(w*dw, 6)
        y = round(y*dh, 6)
        h = round(h*dh, 6)
        return (x,y,w,h)

def categorize(category):
    if '토마토 정상' in category:
        return '0'
    elif '토마토 잎마름병' in category:
        return '1'
    else: 
        return 'False'


file_lists = glob.glob(r'C:/encore_kdh/Yolo_Data/Training/형광등/**/**/*.Json', recursive=True)

for path in file_lists:
    json_name = path.split('.Json')[0]

    with open(f'{path}', encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    bound = data['Bounding']
    size = data['RESOLUTION'].split('*')
    size=list(map(float,size))


    i=0
    while i < len(bound):
        type = categorize(bound[i]['DETAILS'])

        if type !='False' and bound[i]['Drawing'] == 'BOX':
                box =[bound[i]['x1'], bound[i]['x2'], bound[i]['y1'], bound[i]['y2']]
                box=list(map(float, box))

                yolo_bound = list(map(str,convert(size,box)))
                result = type+' '+yolo_bound[0]+' '+yolo_bound[1]+' '+yolo_bound[2]+' '+yolo_bound[3]+'\n'

                if i==0:
                    with open(f'{json_name}.txt', 'w') as f:
                        f.write(result)
                else:
                    with open(f'{json_name}.txt', 'a') as f:
                        f.write(result)        

        i+=1

    f.close()