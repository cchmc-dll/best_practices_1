import cv2
import yaml
from imutils import paths
import argparse
import pickle
import os
#from src.utils import save_object
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
def resize_pad(input_image,desired_size,toRGB): 
        im = input_image
        if toRGB:
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        
        old_size = im.shape[:2] # old_size is in (height, width) format
        ratio = float(desired_size)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])
        # new_size should be in (width, height) format

        im = cv2.resize(im, (new_size[1], new_size[0]))
        delta_w = desired_size - new_size[1]
        delta_h = desired_size - new_size[0]
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)
        color = [0, 0, 0]
        new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
            value=color)
        return new_im
               
def main(config): 
    # Get input
    imfiles = [f for f in os.listdir(config['data']["data_dir"]) if not f.startswith('.')]
    data = []
    
    # Process
    for f in imfiles:
        if not f.startswith('.'):
            im = cv2.imread(os.path.join(config['data']['data_dir'],f))
            new_im = resize_pad(im,config['desired_size'],config['toRGB'])
            data.append(new_im)

    # Create Output
    if config['output']['format'] == 'png':      
        outdir = config['data']['output_dir']
        os.makedirs(outdir,exist_ok=True)
        for f,d in zip(imfiles,data):
            cv2.imwrite(os.path.join(outdir,f), d)
    elif config['output']['format'] == 'pkl':
        outdir = config['data']['pkl_dir']
        os.makedirs(outdir,exist_ok=True)
        save_object(data,os.path.join(outdir,'resized_output.pkl'))
    
    print('resize_pad complete')
    return data
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Configuration file to run resize_pad()')
    parser.add_argument('--config', dest='config', required=True)
    args = parser.parse_args()
    with open(args.config) as conf_file:
        config = yaml.safe_load(conf_file)
    
    data = main(config)
