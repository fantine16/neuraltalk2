#-*-coding:utf-8-*-import json
import json
import argparse
import os
import sys

def get_image_set(sis_test, sis_train, sis_val):

    print('计算SIND数据集全部图像的字典...')
    images_set = {}
    for term in sis_test['images']:
        image_id = term['id'].encode('utf-8')
        images_set[image_id] = {}
        try:
            url = term['url_o']
        except:
            url = term['url_m']
        url = url.encode('utf-8')
        images_set[image_id]['imagename'] = url.split('/')[-1]
        images_set[image_id]['split'] = 'test'
    for term in sis_train['images']:
        image_id=term['id'].encode('utf-8')
        images_set[image_id] = {}
        try:
            url = term['url_o']
        except:
            url = term['url_m']
        url = url.encode('utf-8')
        images_set[image_id]['imagename'] = url.split('/')[-1]
        images_set[image_id]['split'] = 'train'
    for term in sis_val['images']:
        image_id=term['id'].encode('utf-8')
        images_set[image_id] = {}
        try:
            url = term['url_o']
        except:
            url = term['url_m']
        url = url.encode('utf-8')
        images_set[image_id]['imagename'] = url.split('/')[-1]
        images_set[image_id]['split'] = 'val'
    return images_set

def getDii(dii_test,dii_train,dii_val,image_set):
    files_val = os.listdir('/datacenter/storytelling/dataset/val')
    files_train = os.listdir('/datacenter/storytelling/dataset/train')
    files_test = os.listdir('/datacenter/storytelling/dataset/test')

    dii_train_cap = []
    dii_test_cap = []
    dii_val_cap = []

    for term in dii_train['annotations']:
        id = term[0]['photo_flickr_id'].encode('utf-8')
        imagename = image_set[id]['imagename']
        if imagename in files_train:
            t={}
            t['id'] = id
            t['file_path']='/datacenter/storytelling/dataset/train/'+imagename
            t['captions']=[]
            t['captions'].append(term[0]['original_text'].encode('utf-8'))
            dii_train_cap.append(t)

    for term in dii_test['annotations']:
        id = term[0]['photo_flickr_id'].encode('utf-8')
        imagename = image_set[id]['imagename']
        if imagename in files_test:
            t = {}
            t['id'] = id
            t['file_path'] = '/datacenter/storytelling/dataset/test/' + imagename
            t['captions'] = []
            t['captions'].append(term[0]['original_text'].encode('utf-8'))
            dii_test_cap.append(t)

    for term in dii_val['annotations']:
        id = term[0]['photo_flickr_id'].encode('utf-8')
        imagename = image_set[id]['imagename']
        if imagename in files_val:
            t = {}
            t['id'] = id
            t['file_path'] = '/datacenter/storytelling/dataset/val/' + imagename
            t['captions'] = []
            t['captions'].append(term[0]['original_text'].encode('utf-8'))
            dii_val_cap.append(t)

    dii_cap = dii_train_cap+dii_test_cap+dii_val_cap
    return dii_cap


def main(params):

    dii_test = json.load(open(params['input_dii_test'], 'r'))
    dii_train = json.load(open(params['input_dii_train'], 'r'))
    dii_val = json.load(open(params['input_dii_val'], 'r'))
    image_set = get_image_set(dii_test, dii_train, dii_val)
    dii_cap = getDii(dii_test, dii_train, dii_val, image_set)
    json.dump(dii_cap, open(params['output_json'], 'w'))







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_root', default='', help='root file folder of test/train/val images')
    parser.add_argument('--input_dii_test', default='sind_dii/test.description-in-isolation.json', help='input sis test json file')
    parser.add_argument('--input_dii_train', default='sind_dii/train.description-in-isolation.json', help='input sis train json file')
    parser.add_argument('--input_dii_val', default='sind_dii/val.description-in-isolation.json', help='input sis val json file')
    parser.add_argument('--output_json', default='sind/dii_raw_set.json', help='output the preprocessed sis data json file')

    args = parser.parse_args()
    params = vars(args)  # convert to ordinary dict
    print 'parsed input parameters:'
    print json.dumps(params, indent=2)
    main(params)

