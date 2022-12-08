import json
import glob

# 좌표값을 yolo 형식으로 변환하는 함수 구해옴
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


# json 파일에서 disease value에 따라 리스트 위치값으로 변환하는 함수
# 일단 토마토 0, 15만 구분
# 0은 정상, 15는 질병
def categorize(category):  

    if category == 0:
        return '0'
    elif category == 15:
        return '1'
    else: 
        return 'False'
        

# 휴.. 힘들다..
# 양이 많으니 폴더때 마다 지정해서 하는 걸로

#폴더 안에 있는 모든 json 파일을 리스트로 저장
file_lists = glob.glob(r'F:/Big_Data/Yolo_Data/tomato_tra/**/**/*.Json', recursive=True)

# json 파일을 하나씩 읽어서 txt 파일로 변환
for path in file_lists:
    json_name = path[:-9]

    with open(f'{path}', encoding='utf-8') as f:
       data = json.load(f)
       f.close()
    
    bound = data['annotations']
    point_ = bound['points']
    point = point_[0]  

    # data 에서 description 에서 width, height value 리스트로 write
    size = list()
    size.append(data['description']['width'])
    size.append(data['description']['height'])
    
    # disease value에 따라 0, 1로 변환    
    type = categorize(bound['disease'])

    if type !='False':
                
        # 좌표값을 yolo 형식으로 변환
               
        x1 = point['xtl']
        x2 = point['xbr']
        y1 = point['ytl']
        y2 = point['ybr']

        box = [x1, x2, y1, y2]

        yolo_bound = list(map(str,convert(size,box)))
        result = type+' '+yolo_bound[0]+' '+yolo_bound[1]+' '+yolo_bound[2]+' '+yolo_bound[3]+'\n'

        with open(f'{json_name}.txt', 'w') as f:
            f.write(result)

        f.close()
