from plots import plot_one_box, xywh2xyxy
import cv2
import json
import numpy as np
import os

# def plot_img(filename, json_file):
#     im0 = cv2.imread(filename)
#     with open(json_file, 'r', encoding='utf8')as fp:
#         json_data = json.load(fp)

#         for i in range(len(json_data)):
#             image_id = json_data[i]['image_id']
#             person_id = json_data[i]['person_id']
#             kpts = json_data[i]['keypoints']
            
#             kpts = list(map(float, kpts))
#             kpts = list(map(int, kpts))
#             xyxy = np.array(json_data[i]['bbox'])#.reshape((-1, 4))
#             # xyxy = xywh2xyxy(xywh)
#             # xyxy = xyxy.reshape((4,))
#             action_category = json_data[i]['action_category']
#             label = 'person'

#             plot_one_box(xyxy, im0, label=label, kpt_label=True, kpts=kpts, steps=2, orig_shape=im0.shape[:2])
#     cv2.imshow(filename, im0)
#     cv2.waitKey(0)


def plot_img(filename, json_file):
    im0 = cv2.imread(filename)
    color = {"sitting":[255,0,0],"standing":[0,255,0],"lying":[0,0,255],"other":None}
    with open(json_file, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

        xyxy = {}
        action = {}
        kpts = {}

        max_person_id = 0
        for i in range(len(json_data['shapes'])):
            person_id = json_data['shapes'][i]['group_id']
            max_person_id = max(person_id, max_person_id)
            if json_data['shapes'][i]['shape_type'] == 'rectangle':
                xyxy[person_id] = np.array(json_data['shapes'][i]['points'])
                xyxy[person_id] = xyxy[person_id].reshape((4,))
                action[person_id] = json_data['shapes'][i]['label']
            else:
                if person_id not in kpts.keys():
                    kpts[person_id] = [0] * 17 * 2
                else:
                    kpts[person_id][int(json_data['shapes'][i]['label'])*2] = json_data['shapes'][i]['points'][0][0]
                    kpts[person_id][int(json_data['shapes'][i]['label'])*2+1] = json_data['shapes'][i]['points'][0][1]
        
        for i in range(1,max_person_id+1):
            xyxy[i] = list(map(int, xyxy[i]))
            kpts[i] = list(map(int, kpts[i]))
            # print(xyxy[i], kpts[i])
            # print(action[i])
            # print(color[action[i]])
            # print(im0.shape[:2])
            
            plot_one_box(xyxy[i], im0, color=color[action[i]] ,label=action[i], kpt_label=True, kpts=kpts[i], steps=2, orig_shape=im0.shape[:2])
    cv2.imshow(filename, im0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def json2txt(json_file, txt_file):

    f=open(txt_file,"w")

    with open(json_file, 'r', encoding='utf8')as fp:
        print(fp)
        json_data = json.load(fp)

        xyxy = {}
        action = {}
        kpts = {}

        max_person_id = 0
        # print(max_person_id)
        for i in range(len(json_data['shapes'])):
            person_id = json_data['shapes'][i]['group_id']
            # print(person_id, json_data['shapes'][i]['label'])
            max_person_id = max(person_id, max_person_id)
            # print(max_person_id)
            if json_data['shapes'][i]['shape_type'] == 'rectangle':
                xyxy[person_id] = np.array(json_data['shapes'][i]['points'])
                xyxy[person_id] = xyxy[person_id].reshape((4,))
                action[person_id] = json_data['shapes'][i]['label']
            else:
                if person_id not in kpts.keys():
                    kpts[person_id] = [0] * 17 * 2
                else:
                    kpts[person_id][int(json_data['shapes'][i]['label'])*2] = json_data['shapes'][i]['points'][0][0]
                    kpts[person_id][int(json_data['shapes'][i]['label'])*2+1] = json_data['shapes'][i]['points'][0][1]
        
        # print(max_person_id)
        for i in range(1,max_person_id+1):
            xyxy[i] = list(map(int, xyxy[i]))
            kpts[i] = list(map(int, kpts[i]))
            line = [0] + xyxy[i] + kpts[i]
            
            f.write(str(line))
            # plot_one_box(xyxy[i], im0, color=color[action[i]] ,label=action[i], kpt_label=True, kpts=kpts[i], steps=2, orig_shape=im0.shape[:2])
    f.close()
    # cv2.imshow(filename, im0)
    # cv2.waitKey(0)

if __name__ == "__main__":
    img_path = "./images/"
    json_path = "./annotations/"
    txt_path = "./labels/"

    for json_name in os.listdir(json_path):
        if json_name.endswith('.md'):
            continue
        jpg_name = json_name.replace('.json','.jpg')
        txt_name = json_name.replace('.json','.txt')
        filename = img_path + jpg_name
        json_file = json_path + json_name
        txt_file = txt_path + txt_name

        # json2txt(json_file, txt_file)
        plot_img(filename, json_file)